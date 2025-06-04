from django.db import connection
from django.http import JsonResponse
from django.shortcuts import redirect, render
from capymerch.models import Location
from datetime import date, timedelta


def index(request):
    return render(request, "index.html")


def search_locations(request):
    locations = []
    q = request.GET.get('q', '').strip()

    if q:
        try:
            # Simple raw SQL vulnerable to injection
            sql = f"""
                SELECT * FROM capymerch_location
                WHERE location LIKE '%{q}%'
            """
            locations = Location.objects.raw(sql)
        except Exception as e:
            print(f"[ERROR] SQL failed: {e}")

    return render(request, 'search_locations.html', {
        'locations': locations,
        'q': q,
    })


def seed():
    Location.objects.all().delete()
    locations = [
        ("CHIJMES", "A capybara-friendly tranquil city spot.", 5,
         "capy_chijmes.jpg", date.today() - timedelta(days=210)),
        ("Asian Civilisations Museum", "Capybaras love heritage too.",
         5, "capy_acm.jpg", date.today() - timedelta(days=180)),
        ("Merlion Park", "Touristy but capybaras don't mind.", 5,
         "capy_merlion.jpg", date.today() - timedelta(days=150)),
        ("Botanic Gardens", "Great for morning capy walks.",
         4, "", date.today() - timedelta(days=130)),
        ("Bukit Timah Reserve", "For the adventurous capybaras.",
         4, "", date.today() - timedelta(days=110)),
        ("East Coast Park", "Capybaras chill by the sea breeze.", 3,
         "", date.today() - timedelta(days=100)),
        ("Capy Cafe", "Cappuccino and capybaras guaranteed.",
         4, "", date.today() - timedelta(days=95)),
        ("Jurong Lake Gardens", "The quiet lake draws calm capys.",
         4, "", date.today() - timedelta(days=90)),
        ("MacRitchie Reservoir", "Capybaras like trails too.",
         3, "", date.today() - timedelta(days=85)),
        ("Sentosa Beach", "Capys love sand and sun!",
         4, "", date.today() - timedelta(days=80)),
        ("Labrador Nature Reserve", "Historic & peaceful.", 4,
         "", date.today() - timedelta(days=75)),
        ("Capy HQ", "Secret society of Singaporean capybaras.",
         4, "", date.today() - timedelta(days=70)),
        ("Mount Faber", "For capys that love a view.",
         3, "", date.today() - timedelta(days=65)),
        ("Fort Canning", "Underground capybara meeting spot.",
         4, "", date.today() - timedelta(days=60)),
        ("Capy Express", "Mini train for capys, big vibes.",
         4, "", date.today() - timedelta(days=55)),
        ("Yishun Riverwalk", "Danger zone? Not for capys!",
         2, "", date.today() - timedelta(days=50)),
        ("Southern Ridges", "Capybaras love high walks.",
         4, "", date.today() - timedelta(days=45)),
        ("Pasir Ris Park", "Mud spa for capys.",
         4, "", date.today() - timedelta(days=40)),
        ("Raffles Marina", "Capys sail too.", 3,
         "", date.today() - timedelta(days=35)),
        ("HortPark", "Floral paradise for herbivorous friends.",
         4, "", date.today() - timedelta(days=30)),
    ]

    for loc_name, desc, rating, image, dt in locations:
        Location.objects.create(
            location=loc_name,
            description=desc,
            rating=rating,
            image=image,
            date=dt,
        )


def reset(request):
    if request.method == "POST":
        confirm = request.POST.get('confirm')

        if confirm != "confirm":
            return JsonResponse({"success": False})

        seed()
        return redirect("/")
    else:
        return render(request, "reset.html")
