import os
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException, Query, Request, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Portal Maestro de Viajes Familiares - Brújula API",
    description="Motor backend de recálculo dinámico de precios, fechas, ocupantes y calendario anual de puentes familiares.",
    version="2.0.0"
)

# Permitir CORS para desarrollo o consumo externo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Montar directorios estáticos de imágenes
static_dirs = [
    "img",
    "img_alsacia",
    "img_budapest",
    "img_nuremberg",
    "img_rumania",
    "img_sansebastian"
]

for sdir in static_dirs:
    dir_path = os.path.join(BASE_DIR, sdir)
    if os.path.isdir(dir_path):
        app.mount(f"/{sdir}", StaticFiles(directory=dir_path), name=sdir)

@app.get("/", response_class=FileResponse)
async def serve_root():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/index.html", response_class=FileResponse)
async def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

# Modelos Pydantic
class RecalculateRequest(BaseModel):
    destination: str = Field(..., description="Identificador del destino: alsacia, nuremberg, budapest, italia, rumania, sanseb")
    checkin: str = Field(..., description="Fecha de ida formato AAAA-MM-DD")
    checkout: str = Field(..., description="Fecha de vuelta formato AAAA-MM-DD")
    adults: int = Field(default=2, ge=1, le=10, description="Número de adultos")
    children: int = Field(default=1, ge=0, le=10, description="Número de niños")
    child_age: int = Field(default=4, ge=0, le=17, description="Edad del niño")

# Parámetros base de cada destino
DESTINATION_CONFIG = {
    "sanseb": {
        "name": "San Sebastián & Caserío Erreteneko (Navarra)",
        "airport_code": "EAS",
        "booking_dest": "San+Sebastian",
        "is_car_trip": True,
        "base_fuel": 135.0,
        "base_lodging_per_night": 110.0,
        "food_per_person_day": 35.0,
        "activities_per_child": 10.0,
        "fixed_transporte": 0.0
    },
    "alsacia": {
        "name": "Alsacia (Estrasburgo, Colmar, Eguisheim, Riquewihr)",
        "airport_code": "BSL",
        "booking_dest": "Colmar",
        "is_car_trip": False,
        "base_flight_peak": 150.0,
        "base_flight_low": 75.0,
        "base_hotel_peak": 240.0,
        "base_hotel_low": 95.0,
        "car_rental_per_day": 35.0,
        "fuel_estimate": 45.0,
        "food_per_person_day": 30.0,
        "activities_per_child": 15.0
    },
    "nuremberg": {
        "name": "Núremberg & Christkindlesmarkt (Baviera)",
        "airport_code": "NUE",
        "booking_dest": "Nuremberg",
        "is_car_trip": False,
        "base_flight_peak": 266.0,
        "base_flight_low": 110.0,
        "base_hotel_peak": 193.0,
        "base_hotel_low": 95.0,
        "transit_ticket_per_pax_day": 6.0,
        "food_per_person_day": 38.0,
        "activities_per_child": 12.0
    },
    "budapest": {
        "name": "Budapest & Mercadillos del Danubio",
        "airport_code": "BUD",
        "booking_dest": "Budapest",
        "is_car_trip": False,
        "base_flight_peak": 233.0,
        "base_flight_low": 90.0,
        "base_hotel_peak": 190.0,
        "base_hotel_low": 85.0,
        "transit_ticket_per_pax_day": 7.0,
        "food_per_person_day": 33.0,
        "activities_per_child": 15.0
    },
    "italia": {
        "name": "Italia Mágica (Venecia, Florencia, Pisa)",
        "airport_code": "VCE",
        "booking_dest": "Venice",
        "is_car_trip": False,
        "base_flight_peak": 135.0,
        "base_flight_low": 65.0,
        "base_hotel_peak": 80.0,
        "base_hotel_low": 55.0,
        "trains_per_adult": 38.0,
        "trains_per_child": 0.0, # Frecciarossa Bimbi Gratis
        "food_per_person_day": 28.0,
        "activities_per_child": 10.0
    },
    "rumania": {
        "name": "Transilvania Nevada (Castillos de Drácula, Sibiu, Cluj)",
        "airport_code": "CLJ",
        "booking_dest": "Brasov",
        "is_car_trip": False,
        "base_flight_peak": 130.0,
        "base_flight_low": 55.0,
        "base_hotel_peak": 76.0,
        "base_hotel_low": 45.0,
        "suv_rental_per_day": 37.0,
        "fuel_estimate": 75.0,
        "food_per_person_day": 26.0,
        "activities_per_child": 10.0
    }
}

def analyze_seasonality(dt_in: date, dt_out: date) -> Dict[str, Any]:
    """Detecta estacionalidad y factor de sobrecoste o ahorro según la fecha."""
    m_in = dt_in.month
    d_in = dt_in.day
    
    # 1. Superpuente de la Constitución / Inmaculada (4 al 9 de Diciembre)
    if m_in == 12 and 3 <= d_in <= 9:
        return {
            "season": "peak_bridge_december",
            "label": "Superpuente de Diciembre (Temporada Máxima Navideña)",
            "multiplier": 1.0, # Tarifa base del puente ya cotizada
            "savings_pct": 0,
            "badge_color": "#EF4444",
            "tip": "Tarifa de puente festivo español. Si podéis viajar el fin de semana previo (20-23 o 27-30 Nov), ahorraríais entre 350 € y 600 €."
        }
    
    # 2. Finales de Noviembre (Mercadillos Abiertos con Tarifas Bajas)
    if (m_in == 11 and d_in >= 15) or (m_in == 12 and d_in < 3):
        return {
            "season": "smart_advent_november",
            "label": "Apertura Temprana de Adviento (Ventana Óptima de Ahorro)",
            "multiplier": 0.62,
            "savings_pct": 38,
            "badge_color": "#10B981",
            "tip": "¡Excelente elección! Los mercadillos y luces están inaugurados al 100%, pero los vuelos y hoteles son hasta un 40% más baratos que en el puente."
        }
    
    # 3. Fin de Año / Año Nuevo (30 Dic al 4 Ene)
    if (m_in == 12 and d_in >= 29) or (m_in == 1 and d_in <= 4):
        return {
            "season": "new_year_festive",
            "label": "Año Nuevo & Festividad de Invierno",
            "multiplier": 0.95,
            "savings_pct": 5,
            "badge_color": "#F59E0B",
            "tip": "Temporada de celebración festiva. Muy buena ocupación, ambientes decorados y precios moderadamente altos."
        }
        
    # 4. Enero tras Reyes / Febrero (Valle de Temporada Baja)
    if (m_in == 1 and d_in >= 8) or m_in == 2:
        return {
            "season": "low_season_winter",
            "label": "Valle Invernal de Temporada Baja",
            "multiplier": 0.55,
            "savings_pct": 45,
            "badge_color": "#059669",
            "tip": "Tarifas mínimas anuales tanto en aerolíneas como en hoteles céntricos. La mejor relación calidad-precio."
        }
        
    # 5. Resto del año (Primavera / Otoño Estándar)
    return {
        "season": "regular_season",
        "label": "Temporada Estándar",
        "multiplier": 0.75,
        "savings_pct": 25,
        "badge_color": "#3B82F6",
        "tip": "Tarifas regulares sin suplementos festivos españoles."
    }

# ----------------- ENDPOINTS -----------------

@app.api_route("/", methods=["GET", "HEAD"])
def serve_index():
    index_file = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    raise HTTPException(status_code=404, detail="index.html no encontrado")

@app.api_route("/health", methods=["GET", "HEAD"])
@app.api_route("/api/health", methods=["GET", "HEAD"])
def health_check():
    return {
        "status": "online",
        "app": "Portal Maestro de Viajes Familiares - Brújula",
        "environment": "Render Cloud Platform",
        "destinations_available": list(DESTINATION_CONFIG.keys()),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/recalculate")
def recalculate_trip(req: RecalculateRequest):
    dest_key = req.destination.lower().strip()
    if dest_key not in DESTINATION_CONFIG:
        raise HTTPException(
            status_code=400, 
            detail=f"Destino no reconocido: '{req.destination}'. Opciones: {list(DESTINATION_CONFIG.keys())}"
        )
        
    try:
        dt_in = datetime.strptime(req.checkin, "%Y-%m-%d").date()
        dt_out = datetime.strptime(req.checkout, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Utiliza AAAA-MM-DD (ej: 2026-12-05)")
        
    nights = (dt_out - dt_in).days
    if nights < 1:
        raise HTTPException(status_code=400, detail="La fecha de vuelta (checkout) debe ser posterior a la de ida (checkin).")
    if nights > 30:
        raise HTTPException(status_code=400, detail="El rango máximo permitido es de 30 noches.")
        
    cfg = DESTINATION_CONFIG[dest_key]
    season = analyze_seasonality(dt_in, dt_out)
    mult = season["multiplier"]
    
    total_pax = req.adults + req.children
    days = nights + 1
    
    breakdown_items = []
    total_cost = 0.0
    
    # 1. TRANSPORTE / VUELOS
    if cfg.get("is_car_trip", False):
        # Viaje en coche (Volvo XC60): Combustible y peajes
        fuel = cfg["base_fuel"]
        breakdown_items.append({
            "concept": "⛽ Combustible Volvo XC60",
            "detail": f"Ruta completa Alcalá ⇄ Destino (~1.000 km en carretera)",
            "amount": round(fuel, 2)
        })
        total_cost += fuel
    else:
        # Vuelos directos MAD ⇄ Destino
        flight_unit = (cfg["base_flight_low"] + (cfg["base_flight_peak"] - cfg["base_flight_low"]) * mult)
        # Los niños mayores de 2 años pagan asiento completo con tarifa similar
        flights_total = flight_unit * total_pax
        breakdown_items.append({
            "concept": f"✈️ Vuelos Directos MAD ⇄ {cfg['airport_code']}",
            "detail": f"{total_pax} billetes i/v con maletas de cabina ({round(flight_unit, 2)} €/persona)",
            "amount": round(flights_total, 2)
        })
        total_cost += flights_total
        
        # Alquiler de vehículo si aplica (Alsacia, Rumanía)
        if "car_rental_per_day" in cfg:
            car_cost = cfg["car_rental_per_day"] * days + cfg.get("fuel_estimate", 0.0)
            breakdown_items.append({
                "concept": "🚗 Alquiler Coche / Seguro / Gasolina",
                "detail": f"{days} días de alquiler con seguro y combustible de ruta",
                "amount": round(car_cost, 2)
            })
            total_cost += car_cost
        elif "suv_rental_per_day" in cfg:
            suv_cost = cfg["suv_rental_per_day"] * days + cfg.get("fuel_estimate", 0.0)
            breakdown_items.append({
                "concept": "🚙 Alquiler SUV + Ruedas Nieve",
                "detail": f"{days} días con seguro a todo riesgo y viñeta",
                "amount": round(suv_cost, 2)
            })
            total_cost += suv_cost
        elif "trains_per_adult" in cfg:
            train_cost = (cfg["trains_per_adult"] * req.adults) + (cfg["trains_per_child"] * req.children)
            breakdown_items.append({
                "concept": "🚅 Trenes Alta Velocidad & Regional",
                "detail": "Frecciarossa Venecia-Florencia (Bimbi Gratis) + Regional",
                "amount": round(train_cost, 2)
            })
            total_cost += train_cost
        elif "transit_ticket_per_pax_day" in cfg:
            transit_cost = cfg["transit_ticket_per_pax_day"] * total_pax * days
            breakdown_items.append({
                "concept": "🚇 Transporte Urbano & Billetes Locales",
                "detail": f"Abono de transporte ilimitado para {days} días ({total_pax} personas)",
                "amount": round(transit_cost, 2)
            })
            total_cost += transit_cost

    # 2. ALOJAMIENTO
    if cfg.get("is_car_trip", False):
        hotel_nightly = cfg["base_lodging_per_night"] * (0.85 if mult < 1.0 else 1.0)
    else:
        hotel_nightly = cfg["base_hotel_low"] + (cfg["base_hotel_peak"] - cfg["base_hotel_low"]) * mult
        
    # Capacidad hotel: si son más de 3 adultos/niños, se añade suplemento de 2ª habitación o suite
    rooms_needed = 1 if total_pax <= 3 else 2
    hotel_total = hotel_nightly * nights * rooms_needed
    
    room_desc = "Habitación triple / familiar con desayuno buffet" if rooms_needed == 1 else "2 habitaciones dobles o apartamento grande con desayuno"
    breakdown_items.append({
        "concept": f"🏨 Alojamiento Estratégico ({nights} Noches)",
        "detail": f"{room_desc} ({round(hotel_nightly, 2)} €/noche)",
        "amount": round(hotel_total, 2)
    })
    total_cost += hotel_total

    # 3. COMIDAS Y GASTRONOMÍA
    food_day_unit = cfg.get("food_per_person_day", 30.0)
    food_total = food_day_unit * (req.adults + req.children * 0.5) * days
    breakdown_items.append({
        "concept": "🍽️ Comidas, Cenas & Gastronomía Típica",
        "detail": f"Almuerzos y cenas en mesones/tabernas locales ({days} días)",
        "amount": round(food_total, 2)
    })
    total_cost += food_total

    # 4. ACTIVIDADES / ATRACCIONES MARCO
    act_child_unit = cfg.get("activities_per_child", 12.0)
    act_total = act_child_unit * max(1, req.children) + 15.0
    breakdown_items.append({
        "concept": "🎠 Actividades Infantiles & Monumentos",
        "detail": "Carruseles, museos, castillos y atracciones infantiles",
        "amount": round(act_total, 2)
    })
    total_cost += act_total

    cost_per_person = total_cost / total_pax if total_pax > 0 else total_cost

    # 5. GENERACIÓN DINÁMICA DE ENLACES DE BÚSQUEDA EN VIVO (DEEP LINKS)
    dest_airport = cfg.get("airport_code", "EAS")
    checkin_str = dt_in.strftime("%Y-%m-%d")
    checkout_str = dt_out.strftime("%Y-%m-%d")
    checkin_nodash = dt_in.strftime("%y%m%d")
    checkout_nodash = dt_out.strftime("%y%m%d")

    google_flights_url = (
        f"https://www.google.com/travel/flights?q=Flights%20to%20{dest_airport}%20from%20MAD%20on%20{checkin_str}%20through%20{checkout_str}"
    )
    
    skyscanner_url = (
        f"https://www.skyscanner.es/transport/vuelos/mad/{dest_airport.lower()}/{checkin_nodash}/{checkout_nodash}/?adultsv2={req.adults}&childrenv2={req.child_age}"
    )

    booking_url = (
        f"https://www.booking.com/searchresults.es.html?ss={cfg.get('booking_dest', 'Europe')}&checkin={checkin_str}&checkout={checkout_str}&group_adults={req.adults}&group_children={req.children}&age={req.child_age}&no_rooms={rooms_needed}"
    )

    return {
        "success": True,
        "destination": dest_key,
        "destination_name": cfg["name"],
        "checkin": checkin_str,
        "checkout": checkout_str,
        "nights": nights,
        "days": days,
        "adults": req.adults,
        "children": req.children,
        "total_pax": total_pax,
        "seasonality": season,
        "breakdown": breakdown_items,
        "total_cost": round(total_cost, 2),
        "cost_per_person": round(cost_per_person, 2),
        "currency": "EUR",
        "links": {
            "google_flights": google_flights_url,
            "skyscanner": skyscanner_url,
            "booking": booking_url
        }
    }

@app.get("/api/calendar/holidays")
def get_holiday_calendar():
    """Devuelve el calendario de puentes y vacaciones 2026 - 2027 para Madrid / Alcalá de Henares."""
    return {
        "year_2026": [
            {
                "id": "todos_santos_2026",
                "name": "Puente de Todos los Santos 2026",
                "dates": "31 Octubre - 2 Noviembre 2026",
                "days": 3,
                "days_off_needed": 0,
                "type": "Puente Festivo Directo (Lunes 2 festivo trasladado)",
                "recommended_trip": "San Sebastián & Caserío en Bera (Coche Volvo XC60)",
                "cost_level": "Bajo / Valle (Excelente relación calidad-precio)",
                "rating": "Verde (Ahorro)",
                "best_plan": "Ruta en coche sin billetes de avión; caserío con chimenea y sidrerías."
            },
            {
                "id": "constitucion_2026",
                "name": "Puente de la Constitución e Inmaculada 2026",
                "dates": "5 - 8 Diciembre 2026",
                "days": 4,
                "days_off_needed": 1,
                "type": "Superpuente Nacional (Sábado a Martes)",
                "recommended_trip": "Núremberg, Budapest o Alsacia (Mercadillos Navideños)",
                "cost_level": "Alto / Pico Festivo",
                "rating": "Rojo (Pico Festivo)",
                "best_plan": "Vuelos directos reservados con antelación para ver mercadillos iluminados y atracciones infantiles."
            },
            {
                "id": "ano_nuevo_2027",
                "name": "Fin de Año & Año Nuevo 2026-2027",
                "dates": "1 - 4 Enero 2027",
                "days": 4,
                "days_off_needed": 0,
                "type": "Festivo Internacional (Viernes 1 a Lunes 4)",
                "recommended_trip": "Italia (Venecia + Florencia) o Transilvania Nevada (Rumanía)",
                "cost_level": "Medio / Moderado",
                "rating": "Amarillo (Moderado)",
                "best_plan": "Vuelos directos económicos y ambiente festivo de Año Nuevo sin suplementos excesivos."
            }
        ],
        "year_2027": [
            {
                "id": "semana_santa_2027",
                "name": "Semana Santa 2027",
                "dates": "25 - 29 Marzo 2027",
                "days": 5,
                "days_off_needed": 0,
                "type": "Semana Santa (Jueves 25 y Viernes 26 festivos)",
                "recommended_trip": "Sur de Europa o Ruta Templada (Toscana, Costa Brava / Carcassonne)",
                "cost_level": "Medio-Alto",
                "rating": "Amarillo (Moderado)",
                "best_plan": "Primavera temprana; agradable para pasear en familia con Marco."
            },
            {
                "id": "puente_mayo_2027",
                "name": "Puente de Mayo 2027",
                "dates": "30 Abril - 3 Mayo 2027",
                "days": 4,
                "days_off_needed": 0,
                "type": "Fiesta de la Comunidad de Madrid (Viernes 1 + Lunes 3 trasladado)",
                "recommended_trip": "Alsacia Primaveral, Selva Negra o Bretaña",
                "cost_level": "Económico (Fuera de temporada alta europea)",
                "rating": "Verde (Ahorro)",
                "best_plan": "Campos en flor, temperaturas suaves y alquiler de coches muy barato."
            },
            {
                "id": "verano_2027",
                "name": "Vacaciones Familiares de Verano 2027",
                "dates": "Julio / Agosto 2027",
                "days": 10,
                "days_off_needed": 5,
                "type": "Vacaciones Principales de Verano",
                "recommended_trip": "Ruta de los Lagos Alpinos & Selva Negra o Cornisa Cantábrica",
                "cost_level": "Planificable con reserva temprana",
                "rating": "Verde / Amarillo",
                "best_plan": "Naturaleza, parques de juegos al aire libre, sin calores sofocantes."
            },
            {
                "id": "pilar_2027",
                "name": "Puente del Pilar 2027",
                "dates": "9 - 12 Octubre 2027",
                "days": 4,
                "days_off_needed": 1,
                "type": "Fiesta Nacional (Martes 12 Octubre)",
                "recommended_trip": "Asturias & Picos de Europa o Pirineo Aragonés en Volvo XC60",
                "cost_level": "Bajo / Tradicional",
                "rating": "Verde (Ahorro)",
                "best_plan": "Otoño dorado, gastronomía de montaña y rutas llanas con Marco."
            },
            {
                "id": "constitucion_2027",
                "name": "Superpuente de la Constitución 2027",
                "dates": "4 - 8 Diciembre 2027",
                "days": 5,
                "days_off_needed": 1,
                "type": "Superpuente de 5 días (Lunes 6 y Miércoles 8 festivos)",
                "recommended_trip": "Viena, Praga o Múnich (Grandes Capitales Navideñas)",
                "cost_level": "Alto si se reserva tarde; Económico si se reserva en Verano",
                "rating": "Verde (con antelación) / Rojo (última hora)",
                "best_plan": "La mejor ventana de 5 días completos para volar a capitales imperiales."
            }
        ]
    }

@app.get("/api/prospeccion")
def get_prospection_matrix():
    """Devuelve la matriz de prospección de precios pico vs valle para los 6 destinos."""
    return {
        "destinations": [
            {
                "id": "alsacia",
                "name": "Alsacia (Mercadillos)",
                "peak_season": "Puente de Diciembre (5-8 Dic)",
                "peak_cost_3pax": 2298.0,
                "optimal_window": "Último finde de Noviembre (20-23 o 27-30 Nov)",
                "optimal_cost_3pax": 1180.0,
                "estimated_savings_euros": 1118.0,
                "savings_percentage": "48%",
                "reason": "Vuelos a Basilea bajan de 160€ a 70€ y hoteles de Colmar pasan de 280€ a 110€."
            },
            {
                "id": "nuremberg",
                "name": "Núremberg (Baviera)",
                "peak_season": "Puente de Diciembre (5-8 Dic)",
                "peak_cost_3pax": 1805.0,
                "optimal_window": "27-30 Noviembre o 11-14 Diciembre",
                "optimal_cost_3pax": 1050.0,
                "estimated_savings_euros": 755.0,
                "savings_percentage": "42%",
                "reason": "Christkindlesmarkt ya inaugurado; plazas de avión y hoteles céntricos a mitad de precio."
            },
            {
                "id": "budapest",
                "name": "Budapest (Hungría)",
                "peak_season": "Puente de Diciembre (5-8 Dic)",
                "peak_cost_3pax": 1434.0,
                "optimal_window": "Mediados de Noviembre o 15-18 Enero",
                "optimal_cost_3pax": 860.0,
                "estimated_savings_euros": 574.0,
                "savings_percentage": "40%",
                "reason": "Vuelos Wizz Air y Ryanair con ofertas valle a menos de 45€ el trayecto."
            },
            {
                "id": "italia",
                "name": "Italia (Venecia, Florencia, Pisa)",
                "peak_season": "Año Nuevo (31 Dic - 4 Ene)",
                "peak_cost_3pax": 940.0,
                "optimal_window": "15-18 Enero o Febrero (pre-Carnaval)",
                "optimal_cost_3pax": 590.0,
                "estimated_savings_euros": 350.0,
                "savings_percentage": "37%",
                "reason": "Tarifas invernales mínimas en Venecia y Florencia; sin aglomeraciones en los puentes."
            },
            {
                "id": "rumania",
                "name": "Transilvania (Castillos & Sibiu)",
                "peak_season": "Año Nuevo (1-4 Ene)",
                "peak_cost_3pax": 1436.0,
                "optimal_window": "Segunda quincena de Enero o Noviembre",
                "optimal_cost_3pax": 820.0,
                "estimated_savings_euros": 616.0,
                "savings_percentage": "43%",
                "reason": "Vuelos Wizz Air directos a Cluj-Napoca por 29€ trayecto y hoteles 4★ por 45€."
            },
            {
                "id": "sanseb",
                "name": "San Sebastián & Caserío en Bera",
                "peak_season": "Puente de Diciembre (5-8 Dic)",
                "peak_cost_3pax": 749.0,
                "optimal_window": "Cualquier fin de semana de Otoño o Invierno",
                "optimal_cost_3pax": 520.0,
                "estimated_savings_euros": 229.0,
                "savings_percentage": "30%",
                "reason": "Tarifa plana de caserío rural; ahorro en menús y aparcamientos sin masificación."
            }
        ]
    }


# ==============================================================================
# GESTIÓN Y PERSISTENCIA DE VIAJES PERSONALIZADOS GENERADOS POR IA
# ==============================================================================
import requests
import json
import re
import hmac
import hashlib
import time
import base64
import uuid

# ----------------- AUTENTICACIÓN Y GESTIÓN DE USUARIOS -----------------
USERS_FILE = os.path.join(BASE_DIR, "users.json")
PHOTOS_FILE = os.path.join(BASE_DIR, "photos.json")
UPLOADS_DIR = os.path.join(BASE_DIR, "user_uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

AUTH_SECRET_KEY = os.environ.get("AUTH_SECRET_KEY", "brujula_familia_secure_key_2026_x7a")
SALT = "brujula_salt_2026_xyz"

def hash_password(password: str) -> str:
    return hashlib.sha256(f"{SALT}:{password}".encode("utf-8")).hexdigest()

def check_password(password: str, hashed: str) -> bool:
    return hmac.compare_digest(hash_password(password), hashed)

def create_user_token(user_id: str) -> str:
    ts = int(time.time())
    msg = f"{user_id}:{ts}".encode("utf-8")
    sig = hmac.new(AUTH_SECRET_KEY.encode("utf-8"), msg, hashlib.sha256).hexdigest()
    return f"{user_id}.{ts}.{sig}"

def verify_user_token(token: str) -> Optional[str]:
    if not token or "." not in token:
        return None
    parts = token.split(".")
    if len(parts) != 3:
        return None
    user_id, ts_str, sig = parts
    try:
        ts = int(ts_str)
        # Token válido durante 90 días
        if time.time() - ts > 90 * 86400:
            return None
        msg = f"{user_id}:{ts}".encode("utf-8")
        expected_sig = hmac.new(AUTH_SECRET_KEY.encode("utf-8"), msg, hashlib.sha256).hexdigest()
        if hmac.compare_digest(sig, expected_sig):
            return user_id
    except Exception:
        return None
    return None

def init_default_users():
    if not os.path.isfile(USERS_FILE):
        default_users = [
            {
                "id": "adrian",
                "username": "adrian",
                "name": "Adrián Navarro",
                "password_hash": hash_password("1234"),
                "avatar": "👨‍💼",
                "role": "admin",
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "maripaz",
                "username": "maripaz",
                "name": "Maripaz",
                "password_hash": hash_password("1234"),
                "avatar": "👩‍🦰",
                "role": "user",
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "marco",
                "username": "marco",
                "name": "Marco (4 años)",
                "password_hash": hash_password("1234"),
                "avatar": "👦",
                "role": "user",
                "created_at": datetime.now().isoformat()
            }
        ]
        save_users(default_users)

def load_users() -> List[Dict[str, Any]]:
    init_default_users()
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error cargando users.json: {e}")
        return []

def save_users(users: List[Dict[str, Any]]) -> None:
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error guardando users.json: {e}")

def get_current_user_from_req(req: Request) -> Optional[Dict[str, Any]]:
    auth_header = req.headers.get("Authorization", "")
    token = None
    if auth_header.startswith("Bearer "):
        token = auth_header[7:].strip()
    if not token:
        token = req.headers.get("X-Auth-Token")
    if not token:
        token = req.query_params.get("token")
        
    if not token:
        return None
        
    user_id = verify_user_token(token)
    if not user_id:
        return None
        
    users = load_users()
    user = next((u for u in users if u["id"] == user_id), None)
    return user

class RegisterRequest(BaseModel):
    username: str
    password: str
    name: str
    avatar: Optional[str] = "👤"

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/api/auth/register")
async def register_endpoint(req: RegisterRequest):
    uname = req.username.strip().lower()
    if not uname or len(uname) < 3:
        raise HTTPException(status_code=400, detail="El nombre de usuario debe tener al menos 3 caracteres.")
    if not req.password or len(req.password) < 3:
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 3 caracteres.")
    
    users = load_users()
    if any(u["username"].lower() == uname for u in users):
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está registrado.")
        
    user_id = re.sub(r'[^a-z0-9_-]', '', uname)
    if not user_id:
        user_id = f"user_{int(time.time())}"
        
    new_user = {
        "id": user_id,
        "username": uname,
        "name": req.name.strip() or uname.capitalize(),
        "password_hash": hash_password(req.password),
        "avatar": req.avatar or "👤",
        "role": "user",
        "created_at": datetime.now().isoformat()
    }
    users.append(new_user)
    save_users(users)
    
    token = create_user_token(user_id)
    safe_user = {k: v for k, v in new_user.items() if k != "password_hash"}
    return {"status": "ok", "user": safe_user, "token": token}

@app.post("/api/auth/login")
async def login_endpoint(req: LoginRequest):
    uname = req.username.strip().lower()
    users = load_users()
    user = next((u for u in users if u["username"].lower() == uname), None)
    if not user or not check_password(req.password, user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos.")
        
    token = create_user_token(user["id"])
    safe_user = {k: v for k, v in user.items() if k != "password_hash"}
    return {"status": "ok", "user": safe_user, "token": token}

@app.get("/api/auth/me")
async def auth_me_endpoint(request: Request):
    user = get_current_user_from_req(request)
    if not user:
        raise HTTPException(status_code=401, detail="No autenticado o sesión expirada.")
    safe_user = {k: v for k, v in user.items() if k != "password_hash"}
    return {"status": "ok", "user": safe_user}

@app.get("/api/auth/users-list")
async def list_available_users():
    users = load_users()
    return {
        "users": [{"id": u["id"], "username": u["username"], "name": u["name"], "avatar": u.get("avatar", "👤")} for u in users]
    }

# ----------------- GESTIÓN DE FOTOS PRIVADAS POR USUARIO -----------------

def load_photos() -> List[Dict[str, Any]]:
    if os.path.isfile(PHOTOS_FILE):
        try:
            with open(PHOTOS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error cargando photos.json: {e}")
            return []
    return []

def save_photos(photos: List[Dict[str, Any]]) -> None:
    try:
        with open(PHOTOS_FILE, "w", encoding="utf-8") as f:
            json.dump(photos, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error guardando photos.json: {e}")

class UploadPhotoRequest(BaseModel):
    title: str = Field(default="Foto de viaje")
    trip_id: Optional[str] = "general"
    trip_name: Optional[str] = "Recuerdos Familiares"
    date_taken: Optional[str] = None
    image_base64: str = Field(..., description="Imagen en formato data:image/...;base64,... o base64 puro")

@app.get("/api/photos")
async def get_user_photos(request: Request):
    user = get_current_user_from_req(request)
    if not user:
        raise HTTPException(status_code=401, detail="Debes iniciar sesión para ver tus fotos privadas.")
        
    photos = load_photos()
    user_photos = [p for p in photos if p.get("user_id") == user["id"]]
    user_photos.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return {
        "user_id": user["id"],
        "user_name": user["name"],
        "photos": user_photos,
        "total": len(user_photos)
    }

@app.post("/api/photos/upload")
async def upload_user_photo(req: UploadPhotoRequest, request: Request):
    user = get_current_user_from_req(request)
    if not user:
        raise HTTPException(status_code=401, detail="Debes iniciar sesión para subir fotos.")
        
    raw_b64 = req.image_base64
    ext = "jpg"
    mime_type = "image/jpeg"
    if "," in raw_b64:
        header_part, data_part = raw_b64.split(",", 1)
        if "image/png" in header_part:
            ext = "png"
            mime_type = "image/png"
        elif "image/webp" in header_part:
            ext = "webp"
            mime_type = "image/webp"
        elif "image/gif" in header_part:
            ext = "gif"
            mime_type = "image/gif"
        raw_b64 = data_part

    try:
        img_bytes = base64.b64decode(raw_b64)
    except Exception:
        raise HTTPException(status_code=400, detail="Formato de imagen base64 inválido.")
        
    if len(img_bytes) > 12 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="La foto supera el tamaño máximo permitido (12 MB).")

    user_dir = os.path.join(UPLOADS_DIR, user["id"])
    os.makedirs(user_dir, exist_ok=True)
    
    photo_id = f"photo_{int(time.time())}_{uuid.uuid4().hex[:6]}"
    filename = f"{photo_id}.{ext}"
    file_path = os.path.join(user_dir, filename)
    
    with open(file_path, "wb") as f:
        f.write(img_bytes)
        
    photo_entry = {
        "id": photo_id,
        "user_id": user["id"],
        "username": user["username"],
        "author_name": user["name"],
        "title": req.title.strip() or "Recuerdo de viaje",
        "trip_id": req.trip_id or "general",
        "trip_name": req.trip_name or "Viaje Familiar",
        "date_taken": req.date_taken or datetime.now().strftime("%Y-%m-%d"),
        "created_at": datetime.now().isoformat(),
        "filename": filename,
        "url": f"/api/photos/file/{user['id']}/{filename}",
        "mime_type": mime_type,
        "size_bytes": len(img_bytes)
    }
    
    photos = load_photos()
    photos.append(photo_entry)
    save_photos(photos)
    
    return {"status": "ok", "photo": photo_entry}

@app.get("/api/photos/file/{user_id}/{filename}")
async def serve_photo_file(user_id: str, filename: str, request: Request):
    user = get_current_user_from_req(request)
    if not user:
        raise HTTPException(status_code=401, detail="Acceso denegado: debes iniciar sesión.")
    if user["id"] != user_id and user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado: solo el propietario puede ver esta foto.")
        
    clean_filename = os.path.basename(filename)
    file_path = os.path.join(UPLOADS_DIR, user_id, clean_filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="Foto no encontrada.")
        
    ext = os.path.splitext(clean_filename)[1].lower()
    media_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".gif": "image/gif"
    }
    media_type = media_types.get(ext, "image/jpeg")
    return FileResponse(file_path, media_type=media_type)

@app.delete("/api/photos/{photo_id}")
async def delete_photo_endpoint(photo_id: str, request: Request):
    user = get_current_user_from_req(request)
    if not user:
        raise HTTPException(status_code=401, detail="No autenticado.")
        
    photos = load_photos()
    photo = next((p for p in photos if p["id"] == photo_id), None)
    if not photo:
        raise HTTPException(status_code=404, detail="Foto no encontrada.")
        
    if photo["user_id"] != user["id"] and user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar esta foto.")
        
    file_path = os.path.join(UPLOADS_DIR, photo["user_id"], photo.get("filename", ""))
    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error eliminando archivo {file_path}: {e}")
            
    photos = [p for p in photos if p["id"] != photo_id]
    save_photos(photos)
    return {"status": "ok", "deleted": photo_id}

# ----------------- VIAJES PERSONALIZADOS -----------------

CUSTOM_TRIPS_FILE = os.path.join(BASE_DIR, "custom_trips.json")

def load_custom_trips() -> List[Dict[str, Any]]:
    if os.path.isfile(CUSTOM_TRIPS_FILE):
        try:
            with open(CUSTOM_TRIPS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error cargando custom_trips.json: {e}")
            return []
    return []

def save_custom_trips(trips: List[Dict[str, Any]]) -> None:
    try:
        with open(CUSTOM_TRIPS_FILE, "w", encoding="utf-8") as f:
            json.dump(trips, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error guardando custom_trips.json: {e}")

@app.get("/api/trips/custom")
async def get_custom_trips(request: Request):
    user = get_current_user_from_req(request)
    trips = load_custom_trips()
    if user:
        return {"trips": [t for t in trips if t.get("user_id") in [user["id"], None, "public"]]}
    return {"trips": trips}

class SaveTripRequest(BaseModel):
    trip: Dict[str, Any]

@app.post("/api/trips/custom")
async def save_custom_trip_endpoint(req: SaveTripRequest, request: Request):
    user = get_current_user_from_req(request)
    trip = req.trip
    trip_id = trip.get("id")
    if not trip_id:
        raise HTTPException(status_code=400, detail="El viaje debe tener un id.")
    if user:
        trip["user_id"] = user["id"]
        trip["author_name"] = user["name"]
    trips = load_custom_trips()
    idx = next((i for i, t in enumerate(trips) if t.get("id") == trip_id), None)
    if idx is not None:
        trips[idx] = trip
    else:
        trips.append(trip)
    save_custom_trips(trips)
    return {"status": "ok", "trip": trip, "total": len(trips)}

@app.delete("/api/trips/custom/{trip_id}")
async def delete_custom_trip_endpoint(trip_id: str, request: Request):
    user = get_current_user_from_req(request)
    trips = load_custom_trips()
    if user:
        target = next((t for t in trips if t.get("id") == trip_id), None)
        if target and target.get("user_id") and target.get("user_id") != user["id"] and user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="No puedes eliminar este viaje.")
    trips = [t for t in trips if t.get("id") != trip_id]
    save_custom_trips(trips)
    return {"status": "ok", "deleted": trip_id, "remaining": len(trips)}

# ==============================================================================
# ENDPOINT DE ASISTENTE INTELIGENTE GEMINI (BRÚJULA AI)
# ==============================================================================

# Cargar .env local si existe (para desarrollo o servidor local)
env_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(env_file):
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

class GeminiMessage(BaseModel):
    role: str = Field(..., description="'user' o 'model'")
    text: str = Field(...)

class GeminiChatRequest(BaseModel):
    message: str = Field(..., description="Consulta del usuario en lenguaje natural")
    history: Optional[List[GeminiMessage]] = Field(default=[], description="Historial previo de la conversación")
    current_tab: Optional[str] = Field(default=None, description="Pestaña actual donde está el usuario")
    marked_vacations: Optional[List[str]] = Field(default=[], description="Días de vacaciones marcados por el usuario")

class GeminiChatResponse(BaseModel):
    reply: str
    actions: List[Dict[str, Any]] = []

BRUJULA_SYSTEM_PROMPT = """
Eres Brújula AI, el asesor inteligente de confianza para la planificación de viajes de la familia de Adrián, Maripaz y su hijo Marco (4 años), residentes en Alcalá de Henares (Madrid).
Viajan habitualmente en su Volvo XC60 para rutas nacionales o en avión desde Madrid-Barajas (Adolfo Suárez) para viajes europeos.
Tu filosofía es 'Bueno, bonito y barato': prospección activa de ahorro, evitando pagar sobrecostes innecesarios en puentes saturados cuando una fecha valle (como finales de noviembre o enero) ofrece los mismos encantos con hasta un 48% de descuento.
Siempre priorizas la seguridad, logística y diversión de Marco (4 años): ritmos tranquilos, atracciones mágicas (dinosaurios, castillos, trenecitos, mercadillos navideños, parques), alojamientos familiares cómodos y pausas frecuentes en coche.

Conocimiento de viajes actuales disponibles en el catálogo base:
1. San Sebastián & Caserío Erreteneko (Navarra): En coche Volvo XC60 (445 km, 4h30m). Presupuesto base 749€ (3 personas). Caserío rural vasco-navarro, bahía de La Concha, Aquarium Donostia, monte Igueldo y paseo en funicular.
2. Alsacia (Estrasburgo, Colmar, Eguisheim, Riquewihr): Vuelos a Basilea (BSL) o Estrasburgo. En puente 2.327€ vs 1.209€ a finales de noviembre (-48% / 1.118€ de ahorro). Mercadillos navideños de cuento, casas de entramado de madera.
3. Núremberg (Baviera): Vuelos directos a NUE o Múnich. En puente 1.805€ vs 1.050€ a finales de noviembre (-42% / 755€ de ahorro). Christkindlesmarkt, Museo del Juguete, Castillo Imperial, tren DB.
4. Budapest (Hungría): Vuelos directos Wizz Air/Ryanair. En puente 1.434€ vs 860€ en temporada valle (-40% / 574€ de ahorro). Tranvía de la Navidad iluminado, balnearios familiares Széchenyi, Castillo de Buda, Parlamento.
5. Italia (Venecia, Florencia, Pisa): Vuelos a Bolonia o Venecia + Frecciarossa. En Año Nuevo 940€ vs 590€ en temporada valle (-37% / 350€ de ahorro). Góndolas, Piazza San Marco, Duomo de Florencia, Torre de Pisa.
6. Transilvania (Rumanía, Cluj-Napoca, Castillo de Bran/Drácula, Castillo de Corvino, Salina Turda): En Año Nuevo 1.436€ vs 820€ en segunda quincena de enero (-43% / 616€ de ahorro). Paisajes nevados, minas de sal con noria subterránea y barcas.

Calendario y festivos de Madrid / Alcalá:
- 2026: Puente de Todos los Santos (1-2 Nov), Puente de la Constitución / Inmaculada (5-8 Dic), Navidad (25 Dic).
- 2027: Reyes (6 Ene), Semana Santa (25-28 Mar), Puente de Mayo (1-3 May), Santos Niños Alcalá (6 Ago), Asunción (15-16 Ago), Fiesta Nacional / Cervantes (9-12 Oct), Todos los Santos (1 Nov), Constitución / Inmaculada (6-8 Dic).

========================================================================
⚡ GENERACIÓN ACTIVA DE NUEVOS VIAJES (INSTRUCCIÓN CRÍTICA):
========================================================================
Cuando el usuario te pida crear, generar, proponer, cotizar o idear un NUEVO VIAJE o DESTINO (por ejemplo: Suiza, Viena, Laponia, Disney París, Praga, Selva Negra, Roma, Copenhague, Tirol, etc.) o cambios sustanciales:
1. Responde en el texto detallando el plan completo: por qué es ideal para Adrián, Maripaz y Marco (4 años), cómo llegar (coche o vuelo desde Barajas), dónde dormir, actividades mágicas para Marco y el presupuesto "Bueno, Bonito y Barato".
2. AL FINAL DE TU MENSAJE, DEBES INCLUIR OBLIGATORIAMENTE un bloque ```actions ... ``` con la acción "create_trip" con todos los datos estructurados para que la web inyecte automáticamente la tarjeta interactiva, el botón en el menú de navegación y la ficha completa del viaje con su itinerario y tabla de costes.

Formato exacto del bloque de acciones para crear un viaje nuevo:
```actions
[
  {
    "action": "create_trip",
    "label": "🌟 Abrir Ficha Creada: Suiza & Alpes Navideños",
    "trip": {
      "id": "suiza",
      "title": "Suiza & Alpes Navideños",
      "emoji": "🇨🇭",
      "tag": "Invierno / Navidad · 4 Días",
      "dates": "5 al 8 Dic 2026",
      "image_url": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?auto=format&fit=crop&w=1200&q=80",
      "summary": "Escapada mágica a Zúrich y Lucerna con paseo en barco por el lago, tren panorámico a la nieve y mercadillos iluminados.",
      "transport_desc": "Vuelo directo Madrid ⇄ Zúrich (Swiss / easyJet, 2h 20m) + pases de tren panorámico",
      "lodging_desc": "Hotel familiar con encanto en Lucerna o Zúrich con desayuno buffet",
      "marco_highlights": "Trenecito de montaña, chocolate caliente suizo, puente medieval Kapellbrücke y tiovivo.",
      "total_cost": 1320,
      "cost_per_person": 440,
      "itinerary": [
        {"day": 1, "title": "Llegada a Zúrich & Mercadillo Central", "desc": "Vuelo directo desde Barajas, tren exprés al centro y visita al gran abeto de cristales Swarovski."},
        {"day": 2, "title": "Lucerna & Barco por el Lago", "desc": "Paseo por el puente medieval Kapellbrücke de madera, paseo en barco y tiovivo junto al lago."},
        {"day": 3, "title": "Subida a la nieve en monte Rigi", "desc": "Ascenso en tren de cremallera tocando nieve suave con Marco y vistas alpinas espectaculares."},
        {"day": 4, "title": "Mercadillos del Casco Antiguo y Vuelta", "desc": "Compras de dulces artesanos, almuerzo tradicional y vuelo de regreso a Madrid."}
      ],
      "costs_breakdown": [
        {"concept": "Vuelos directos I/V (3 plazas)", "total": "540 €"},
        {"concept": "Alojamiento (3 noches familiar)", "total": "450 €"},
        {"concept": "Pases de tren suizo / transporte", "total": "180 €"},
        {"concept": "Comidas y meriendas tradicionales", "total": "280 €"},
        {"concept": "Actividades y funicular para Marco", "total": "70 €"}
      ]
    }
  }
]
```

Para consultas sobre los viajes ya existentes o fechas en el calendario:
- `{"action": "open_tab", "tab": "alsacia", "label": "📍 Abrir ficha de Alsacia"}`
- `{"action": "simulate_dates", "destination": "alsacia", "checkin": "2026-11-20", "checkout": "2026-11-23", "label": "⚡ Cotizar en Simulador"}`
- `{"action": "open_calendar", "year": 2026, "month": 11, "label": "📅 Ver Diciembre en Calendario"}`
"""

@app.post("/api/gemini/chat", response_model=GeminiChatResponse)
async def gemini_chat(req: GeminiChatRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY no configurada en el servidor.")

    contents = []
    
    ctx_parts = [BRUJULA_SYSTEM_PROMPT]
    if req.current_tab:
        ctx_parts.append(f"Nota de contexto: El usuario está viendo actualmente la pestaña '{req.current_tab}'.")
    if req.marked_vacations:
        ctx_parts.append(f"Días de vacaciones que Adrián y Maripaz tienen marcados en su calendario: {', '.join(req.marked_vacations)}.")

    for h in req.history[-6:]:
        role = "user" if h.role == "user" else "model"
        contents.append({"role": role, "parts": [{"text": h.text}]})

    contents.append({"role": "user", "parts": [{"text": req.message}]})

    payload = {
        "systemInstruction": {"parts": [{"text": "\n\n".join(ctx_parts)}]},
        "contents": contents,
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2500
        }
    }

    models = ["gemini-3.5-flash-lite", "gemini-3.5-flash"]
    last_error = None
    response_text = None

    for m in models:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={GEMINI_API_KEY}"
            resp = requests.post(url, json=payload, timeout=22)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates and "content" in candidates[0]:
                    response_text = candidates[0]["content"]["parts"][0]["text"]
                    break
            else:
                last_error = f"{m} HTTP {resp.status_code}: {resp.text[:200]}"
        except Exception as e:
            last_error = f"{m} Exception: {str(e)}"

    if not response_text:
        response_text = f"Hola Adrián y Maripaz. En este momento el servicio de Gemini está tardando en responder ({last_error}). Podéis consultar los precios en tiempo real y el radar de ahorro directamente en la pestaña del viaje o en el Simulador de Fechas."

    actions = []
    action_match = re.search(r"```actions\s*([\s\S]*?)\s*```", response_text)
    if action_match:
        try:
            parsed_actions = json.loads(action_match.group(1))
            if isinstance(parsed_actions, list):
                actions = parsed_actions
        except Exception:
            pass
        response_text = re.sub(r"```actions\s*[\s\S]*?\s*```", "", response_text).strip()

    # Si se generó un nuevo viaje, guardarlo en el almacenamiento de viajes personalizados
    for act in actions:
        if act.get("action") == "create_trip" and "trip" in act:
            t = act["trip"]
            if t.get("id"):
                existing_trips = load_custom_trips()
                idx = next((i for i, item in enumerate(existing_trips) if item.get("id") == t["id"]), None)
                if idx is not None:
                    existing_trips[idx] = t
                else:
                    existing_trips.append(t)
                save_custom_trips(existing_trips)

    return GeminiChatResponse(reply=response_text, actions=actions)
