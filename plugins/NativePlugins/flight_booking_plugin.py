import json
import os
from semantic_kernel.functions import kernel_function

class FlightBookingPlugin:
    def __init__(self):
        # Localización robusta del archivo JSON
        # Buscamos la carpeta 'data' en la raíz del proyecto
        self.data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/flights.json"))
        self._load_flights()

    def _load_flights(self):
        try:
            with open(self.data_path, "r") as f:
                self.flights = json.load(f)
            print(f"DEBUG: [Plugin] {len(self.flights)} vuelos cargados correctamente.")
        except Exception as e:
            print(f"DEBUG: [Error] No se pudo cargar el archivo JSON: {e}")
            self.flights = []

    def _save_flights(self):
        with open(self.data_path, "w") as f:
            json.dump(self.flights, f, indent=2)

    @kernel_function(
        name="search_flights",
        description="Searches for available flights. Returns a list of flights."
    )
    def search_flights(self, destination: str, departure_date: str) -> str:
        # ESTE PRINT ES CLAVE: Si no lo ves en consola, la IA no está usando el plugin
        print(f"DEBUG: [Llamada IA] Buscando en {destination} para el {departure_date}...")
        
        matching = [
            f for f in self.flights
            if f["Destination"].lower() == destination.lower() and f["DepartureDate"] == departure_date
        ]
        
        if not matching:
            return "No flights found for that specific destination and date."
        
        return json.dumps(matching)

    @kernel_function(
        name="book_flight",
        description="Books a flight using the flight ID."
    )
    def book_flight(self, flight_id: int) -> str:
        print(f"DEBUG: [Llamada IA] Intentando reservar ID: {flight_id}")
        
        for f in self.flights:
            if f["Id"] == int(flight_id):
                if f["IsBooked"]:
                    return "Error: This flight is already booked."
                f["IsBooked"] = True
                self._save_flights()
                return f"Success! Flight {flight_id} to {f['Destination']} is now booked."
        
        return f"Error: Flight ID {flight_id} not found."
