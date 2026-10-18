import os
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException, Query
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

@app.get("/")
def serve_index():
    index_file = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    raise HTTPException(status_code=404, detail="index.html no encontrado")

@app.get("/health")
@app.get("/api/health")
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
