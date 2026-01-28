"""
Concert Booking Tools for LangChain Agent
These tools provide functionality for searching, booking, and managing concert tickets.
"""

from langchain.tools import tool
from typing import Optional
from datetime import datetime



# Mock database for demonstration
CONCERTS_DB = [
    {
        "id": 1,
        "artist": "Taylor Swift",
        "venue": "Madison Square Garden",
        "city": "New York",
        "date": "2026-03-15",
        "available_tickets": 500,
        "price_range": {"vip": 500, "standard": 150, "balcony": 75}
    },
    {
        "id": 2,
        "artist": "Coldplay",
        "venue": "Hollywood Bowl",
        "city": "Los Angeles",
        "date": "2026-04-20",
        "available_tickets": 800,
        "price_range": {"vip": 350, "standard": 120, "balcony": 60}
    },
    {
        "id": 3,
        "artist": "Ed Sheeran",
        "venue": "The O2 Arena",
        "city": "London",
        "date": "2026-05-10",
        "available_tickets": 1000,
        "price_range": {"vip": 400, "standard": 100, "balcony": 50}
    },
    {
        "id": 4,
        "artist": "The Weeknd",
        "venue": "United Center",
        "city": "Chicago",
        "date": "2026-06-05",
        "available_tickets": 600,
        "price_range": {"vip": 450, "standard": 130, "balcony": 65}
    },
    {
        "id": 5,
        "artist": "Billie Eilish",
        "venue": "Staples Center",
        "city": "Los Angeles",
        "date": "2026-07-12",
        "available_tickets": 450,
        "price_range": {"vip": 380, "standard": 110, "balcony": 55}
    }
]

ARTIST_INFO = {
    "Taylor Swift": {
        "genre": "Pop/Country",
        "bio": "American singer-songwriter known for narrative songs about her personal life.",
        "albums": ["Folklore", "Evermore", "Midnights", "The Tortured Poets Department"]
    },
    "Coldplay": {
        "genre": "Alternative Rock",
        "bio": "British rock band formed in 1996, known for their atmospheric sound.",
        "albums": ["Parachutes", "A Rush of Blood to the Head", "Viva la Vida", "Music of the Spheres"]
    },
    "Ed Sheeran": {
        "genre": "Pop/Folk",
        "bio": "English singer-songwriter known for his acoustic guitar performances.",
        "albums": ["÷ (Divide)", "× (Multiply)", "= (Equals)", "- (Subtract)"]
    },
    "The Weeknd": {
        "genre": "R&B/Pop",
        "bio": "Canadian singer and songwriter known for his distinctive voice and dark themes.",
        "albums": ["After Hours", "Starboy", "Beauty Behind the Madness", "Dawn FM"]
    },
    "Billie Eilish": {
        "genre": "Alternative Pop",
        "bio": "American singer-songwriter who gained fame with her unique dark pop sound.",
        "albums": ["When We All Fall Asleep, Where Do We Go?", "Happier Than Ever", "Hit Me Hard and Soft"]
    }
}


@tool
def search_concerts(artist: Optional[str] = None, city: Optional[str] = None, date: Optional[str] = None) -> str:
    """
    Search for concerts by artist name, city, or date.
    
    Args:
        artist: Name of the artist or band (optional)
        city: City where the concert takes place (optional)
        date: Date of the concert in YYYY-MM-DD format (optional)
    
    Returns:
        A formatted string with concert search results
    """
    results = CONCERTS_DB.copy()
    
    # Filter by artist
    if artist:
        results = [c for c in results if artist.lower() in c["artist"].lower()]
    
    # Filter by city
    if city:
        results = [c for c in results if city.lower() in c["city"].lower()]
    
    # Filter by date
    if date:
        results = [c for c in results if c["date"] == date]
    
    if not results:
        return "No concerts found matching your criteria."
    
    # Format results
    output = f"Found {len(results)} concert(s):\n\n"
    for concert in results:
        output += f"🎵 {concert['artist']}\n"
        output += f"   📍 Venue: {concert['venue']}, {concert['city']}\n"
        output += f"   📅 Date: {concert['date']}\n"
        output += f"   🎫 Available Tickets: {concert['available_tickets']}\n"
        output += f"   💰 Price Range: ${concert['price_range']['balcony']} - ${concert['price_range']['vip']}\n\n"
    
    return output


@tool
def check_venue_availability(venue_name: str, date: str) -> str:
    """
    Check if a venue is available on a specific date.
    
    Args:
        venue_name: Name of the venue
        date: Date to check in YYYY-MM-DD format
    
    Returns:
        Availability information for the venue
    """
    concerts = [c for c in CONCERTS_DB if venue_name.lower() in c["venue"].lower() and c["date"] == date]
    
    if concerts:
        concert = concerts[0]
        return f"{concert['venue']} is hosting {concert['artist']} on {date}. {concert['available_tickets']} tickets available."
    else:
        return f"{venue_name} appears to be available on {date}. No concerts currently scheduled."


@tool
def get_ticket_prices(artist: str) -> str:
    """
    Get ticket prices for a specific artist's concert.
    
    Args:
        artist: Name of the artist or band
    
    Returns:
        Ticket pricing information
    """
    concerts = [c for c in CONCERTS_DB if artist.lower() in c["artist"].lower()]
    
    if not concerts:
        return f"No concerts found for {artist}."
    
    output = f"Ticket prices for {artist} concerts:\n\n"
    for concert in concerts:
        output += f"📍 {concert['venue']}, {concert['city']} ({concert['date']}):\n"
        output += f"   VIP: ${concert['price_range']['vip']}\n"
        output += f"   Standard: ${concert['price_range']['standard']}\n"
        output += f"   Balcony: ${concert['price_range']['balcony']}\n\n"
    
    return output


@tool
def book_concert_tickets(artist: str, date: str, num_tickets: int, ticket_type: str = "standard") -> str:
    """
    Book tickets for a concert.
    
    Args:
        artist: Name of the artist or band
        date: Date of the concert in YYYY-MM-DD format
        num_tickets: Number of tickets to book
        ticket_type: Type of ticket - 'vip', 'standard', or 'balcony' (default: 'standard')
    
    Returns:
        Booking confirmation or error message
    """
    # Find the concert
    concerts = [c for c in CONCERTS_DB if artist.lower() in c["artist"].lower() and c["date"] == date]
    
    if not concerts:
        return f"No concert found for {artist} on {date}."
    
    concert = concerts[0]
    
    # Check availability
    if concert["available_tickets"] < num_tickets:
        return f"Only {concert['available_tickets']} tickets available. Cannot book {num_tickets} tickets."
    
    # Validate ticket type
    ticket_type = ticket_type.lower()
    if ticket_type not in concert["price_range"]:
        return "Invalid ticket type. Choose from: vip, standard, or balcony."
    
    # Calculate total price
    price_per_ticket = concert["price_range"][ticket_type]
    total_price = price_per_ticket * num_tickets
    
    # Simulate booking (in real app, this would update database)
    booking_id = f"BK{concert['id']}{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    confirmation = f"""
Booking Confirmed!

Booking ID: {booking_id}
Artist: {concert['artist']}
Venue: {concert['venue']}, {concert['city']}
Date: {concert['date']}
Tickets: {num_tickets} x {ticket_type.capitalize()} (${price_per_ticket} each)
Total Amount: ${total_price}

Your tickets will be sent to your email. Enjoy the show! 
"""
    
    return confirmation


@tool
def get_artist_info(artist_name: str) -> str:
    """
    Get information about an artist or band.
    
    Args:
        artist_name: Name of the artist or band
    
    Returns:
        Artist biography and information
    """
    for artist, info in ARTIST_INFO.items():
        if artist_name.lower() in artist.lower():
            output = f"{artist}\n\n"
            output += f"Genre: {info['genre']}\n"
            output += f"Bio: {info['bio']}\n\n"
            output += "Popular Albums:\n"
            for album in info['albums']:
                output += f"  • {album}\n"
            
            # Also show upcoming concerts
            concerts = [c for c in CONCERTS_DB if artist.lower() in c["artist"].lower()]
            if concerts:
                output += "\nUpcoming Concerts:\n"
                for concert in concerts:
                    output += f"  • {concert['city']} - {concert['date']}\n"
            
            return output
    
    return f"Artist information not found for '{artist_name}'."


@tool
def check_date_availability(date: str, city: Optional[str] = None) -> str:
    """
    Check what concerts are available on a specific date.
    
    Args:
        date: Date to check in YYYY-MM-DD format
        city: Optional city to filter by
    
    Returns:
        List of concerts on that date
    """
    concerts = [c for c in CONCERTS_DB if c["date"] == date]
    
    if city:
        concerts = [c for c in concerts if city.lower() in c["city"].lower()]
    
    if not concerts:
        location = f" in {city}" if city else ""
        return f"No concerts scheduled{location} on {date}."
    
    output = f"Concerts on {date}:\n\n"
    for concert in concerts:
        output += f"🎵 {concert['artist']} at {concert['venue']}, {concert['city']}\n"
        output += f"   🎫 {concert['available_tickets']} tickets available\n"
        output += f"   💰 From ${concert['price_range']['balcony']}\n\n"
    
    return output
