from django.db.models import Func, F, Value, CharField
from django.http import JsonResponse
from django.shortcuts import redirect, render
from capymerch.models import Location
from datetime import date, timedelta
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, "index.html")


def locations(request):
    letter = request.GET.get('letter', '').upper()
    date = request.GET.get('date', '')
    results = []

    if letter:
        qs = Location.objects.annotate(
            first_letter=Func(F('location'), Value(1), Value(
                1), function='substr', output_field=CharField())
        ).filter(first_letter__iexact=letter)

        if date:
            qs = qs.filter(date=date)

        results = [loc.location for loc in qs]

    return render(request, 'locations.html', {
        'results': results,
        'letter': letter,
        'date': date,
    })


@csrf_exempt
def search_locations(request):
    locations = []
    q = ''
    if request.method == 'POST':
        q = request.POST.get('q', '').strip()

        try:
            sql = f"""
                SELECT * FROM capymerch_location
                WHERE location LIKE '%{q}%'
            """
            locations = Location.objects.raw(sql)
        except Exception as e:
            locations = []
            print(f"[ERROR] SQL failed: {e}")

    return render(request, 'search_locations.html', {
        'locations': locations,
        'q': q
    })


def seed():
    Location.objects.all().delete()
    locations = [
        ("CHIJMES", "Good ramen can be found here.", 5,
         "capy_chijmes.jpg", date.today() - timedelta(days=210)),
        ("Asian Civilisations Museum", "Not super crowded and touristy unlike other museums.",
         5, "capy_acm.jpg", date.today() - timedelta(days=180)),
        ("Merlion Park", "Bleh.", 5,
         "capy_merlion.jpg", date.today() - timedelta(days=150)),
        ("Botanic Gardens", "Kinda mid.",
         3, "", date.today() - timedelta(days=130)),
        ("Bukit Timah Reserve", "For the adventurous capybaras.",
         4, "", date.today() - timedelta(days=110)),
        ("East Coast Park", "Capybaras chill by the sea breeze.", 4,
         "", date.today() - timedelta(days=100)),
        ("Capy Cafe", "Cappuccino and capybaras guaranteed.",
         4, "", date.today() - timedelta(days=95)),
        ("Jurong Lake Gardens", "The quiet lake draws calm capys.",
         4, "", date.today() - timedelta(days=90)),
        ("MacRitchie Reservoir", "Capybaras like trails too.",
         3, "", date.today() - timedelta(days=85)),
        ("Sentosa Beach", "Capys love sand and sun! And beaches!",
         4, "", date.today() - timedelta(days=80)),
        ("Labrador Nature Reserve", "Historic & peaceful.", 4,
         "", date.today() - timedelta(days=75)),
        ("Mount Faber", "Pull up in a cablecar.",
         3, "", date.today() - timedelta(days=65)),
        ("Fort Canning", "Underground capybara meeting spot. For the sigma ones.",
         4, "", date.today() - timedelta(days=60)),
        ("Capy Express", "Mini train for capys, big vibes.",
         4, "", date.today() - timedelta(days=55)),
        ("Punggol Waterway", "What? Otters?!",
         1, "", date.today() - timedelta(days=50)),
        ("Southern Ridges", "Capybaras love high walks.",
         4, "", date.today() - timedelta(days=45)),
        ("Pasir Ris Park", "This is where they pull up.",
         4, "", date.today() - timedelta(days=40)),
        ("Raffles Marina", "Capybaras love a good soak in the water. Best option since there are no hot springs in Singapore.", 3,
         "", date.today() - timedelta(days=35)),
        ("HortPark", "Great spot to chill.",
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
