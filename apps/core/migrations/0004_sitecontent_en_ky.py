from django.db import migrations

EN = {
    "index_paragraph_1": "The Kyrgyz Republic is mountainous. Over 95% of freight and passenger transport is by road and partly by rail. Therefore the republic needed mid-level specialists skilled in maintaining and operating vehicles and in building roads and railways.",
    "index_paragraph_2": "In 1939 an automotive department was established at the Frunze Industrial Technical School from a single group, training mechanics in vehicle maintenance and repair. The first graduation of 14 students was in 1942.",
    "history_paragraph_1": "The Kyrgyz Republic is mountainous. Over 95% of freight and passenger transport is by road and partly by rail. Therefore the republic needed mid-level specialists skilled in maintaining and operating vehicles and in building roads and railways.",
    "history_paragraph_2": "In 1939 an automotive department was created at the Frunze Industrial Technical School from a single group, training mechanics for vehicle maintenance and repair. The first graduation of 14 people took place in 1942. Bishkek–Osh highway.",
    "history_paragraph_3": "At that time the demand for road-transport specialists was so high that, despite World War II, in 1943 an independent road technical school was established. G. A. Svetlichny became head of the new training center for the automotive and road sectors. Initially the school was located in Frunze opposite the tobacco factory, and then until 1946 in the railway station building. Future teachers P.K. Denisov, T.U. Umarbekov, D.U. Ubyshov studied there. In 1946 the school moved to the first floor of the present construction college. A year later it became the automotive department of the construction-industrial technical school under the Ministry of Construction of the Kyrgyz SSR. After a few years it became clear that the existing system of training mid-level specialists did not meet the republic's needs.",
    "history_paragraph_4": "The idea to revive the road technical school belonged to the Minister of Motor Transport and Highways, Kusain Kolbaev. According to USSR Council of Ministers decree No.1294 of June 29, 1954, the Council of Ministers of the Kyrgyz SSR ordered: complete the academic building in Frunze by September 1, 1957, and open a first-category road technical school with specialties in vehicle operation and repair, road machinery and equipment, and road and bridge construction. Chairman A. Suerkulov.",
    "history_paragraph_5": "To implement this, decree No.209 of June 19, 1957 established a first-category road technical school in Frunze. Admission was announced for the specialties listed above. 1957 is considered the founding year of our college. By Government decree No.743 of December 22, 1997, the school was renamed the Bishkek Automobile-Road Technical School named after Kusain Kolbaev.",
    "history_paragraph_6": "“The First Engineer” — that was Kolbaev’s nickname. Wherever he served he proved a skilled organizer and specialist, making a huge contribution to Kyrgyzstan’s transport and road infrastructure. He devoted great attention to training qualified personnel. The memory of the First Engineer inspires pride and obliges all transport workers to labor diligently, as did this loyal son of Kyrgyzstan.",
    "history_paragraph_7": "Kusain Kolbaev was born on November 25, 1908. In 1925 he was among the first Komsomol members sent to study in Tver. In 1930 he entered the Leningrad Institute of Railway Transport, automobile-road faculty.",
    "history_paragraph_8": "Kusain Kolbaev also went down in history as the person who expanded the road network and transport enterprises. Thanks to his professionalism major routes appeared: Bishkek–Talas, Bishkek–Osh. The hardest years were the 1950s: almost no paved roads, wooden temporary bridges, all work done by hand. In 17 years he provided the republic with paved road junctions and built major reinforced-concrete plants. Under him roads were built: Bishkek–Rybachye–Naryn–Torugart (550 km), around Issyk-Kul (450 km), Taldysu–Santas–Karkyra (100 km), Naryn–Aktalchat–Kazaraman (250 km) and more. He laid the main arteries: Bishkek–Osh, Bishkek–Torugart, Bishkek–Talas.",
}

KY = {
    "index_paragraph_1": "Кыргыз Республикасы тоолуу аймакта жайгашкан. Жүктөрдү жана жүргүнчүлөрдү ташуулардын 95%тен ашығы автомобиль жана жарым-жартылай темир жол транспорту менен жүзөгө ашырылат. Ошондуктан республикага автотранспортту эксплуата-циялоо, автомобиль жолдорун жана темир жолдорду куруу боюнча ыктарга ээ болгон орто звенодогу адистерди даырдоо зарыл болгон.",
    "history_paragraph_1": "Кыргыз Республикасы тоолуу аймакта жайгашкан. Жүктөрдү жана жүргүнчүлөрдү ташуулардын 95%тен ашығы автомобиль жана жарым-жартылай темир жол транспорту менен жүзөгө ашырылат. Ошондуктан республикага автотранспортту эксплуата-циялоо, автомобиль жолдорун жана темир жолдорду куруу боюнча ыктарга ээ болгон орто звенодогу адистерди даырдоо зарыл болгон.",
}


def populate(apps, schema_editor):
    SiteContent = apps.get_model("core", "SiteContent")
    for key, value_en in EN.items():
        obj = SiteContent.objects.filter(key=key).first()
        if obj:
            obj.value_en = value_en
            if key in KY:
                obj.value_ky = KY[key]
            obj.save()


def depopulate(apps, schema_editor):
    SiteContent = apps.get_model("core", "SiteContent")
    for key in EN:
        obj = SiteContent.objects.filter(key=key).first()
        if obj:
            obj.value_en = ""
            obj.value_ky = ""
            obj.save()


class Migration(migrations.Migration):
    dependencies = [("core", "0003_sitecontent_initial_data")]

    operations = [migrations.RunPython(populate, depopulate)]
