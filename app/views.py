from django.shortcuts import render

units = [
    {
        "id": 1,
        "name": "Отдел безопасности и охраны",
        "description": "• Обеспечение надежной защиты объектов филиала от краж, хищений, грабежей, других преступных посягательств и общественных беспорядков;\n• Обеспечение инженерно-технической защиты Филиала;\n• Обеспечение на охраняемых объектах контрольно-пропускного и внутриобъектового режима, предупреждение и пресечение хищений материальных ценностей;\n• Пресечение попыток несанкционированного проникновения на объекты филиала посторонних лиц;\n• Установление порядка допуска сотрудников сторонних организаций, посетителей и транспортных средств на охраняемую территорию;",
        "phone": "8 904 815 31 92",
        "image": "http://localhost:9000/images/1.png"
    },
    {
        "id": 2,
        "name": "Ученый совет",
        "description": "• Рассмотрение вопросов текущей деятельности и развития Филиала в целях обеспечения высокого качества подготовки выпускников;\n• Методическое руководство и координация деятельности Филиала в сфере: учебной работы, научно-исследовательской работы, кадровой и административной работы, социальной работы.",
        "phone": "8 914 825 51 52",
        "image": "http://localhost:9000/images/2.png"
    },
    {
        "id": 3,
        "name": "Отдел инженерной эксплуатации",
        "description": "• Поддержка учебных корпусов, зданий общежитий в состоянии, обеспечивающем их долголетнюю и надежную работу. Для этого подразделение проводит техническую эксплуатацию зданий, профилактику их конструкций, осуществляет проведение текущего ремонта зданий, поддерживать инженерные системы в учебных корпусах и зданиях общежитий в состоянии, обеспечивающем их долголетнюю и надежную работу.\n• Поддержка электротехнических систем в учебных корпусах и зданиях общежитий в состоянии, обеспечивающем их долголетнюю и надежную работу. Для этого подразделение проводит их техническую эксплуатацию и профилактику конструкций, узлов оборудования и приборов.",
        "phone": "8 753 215 35 11",
        "image": "http://localhost:9000/images/3.png"
    },
    {
        "id": 4,
        "name": "Отдел научной и инновационной деятельности",
        "description": "• Координация, организационно-методическая поддержка и контроль выполнения по веществам отраслей НИОКР с целью создания образцов машин, оборудования, материалов, новых технологических процессов, решения важных социальных и экологических задач, совершенствования организации труда и управления.\n• Организация проведения фундаментальных исследований по Программам федерального и регионального правительств, направленных на инновационное развитие Калужского региона.\n• Организация научных, технологических, организационных, финансовых и коммерческих мероприятий, направленных на коммерциализацию накопленных знаний, технологий и оборудования.\n• Содействие повышению качества подготовки специалистов и научно-педагогических кадров, росту квалификации профессорско-преподавательского состава филиала.\n• Организация учета, анализа и оформления результатов научно-технической деятельности Филиала, создание базы данных научно-технических достижений.",
        "phone": "8 324 315 41 32",
        "image": "http://localhost:9000/images/4.png"
    },
    {
        "id": 5,
        "name": "Бухгалтерия",
        "description": "• Исполнение «Учётной политики Университета в соответствии с законодательством о бухгалтерском и налоговом учёте, обеспечивая финансовую устойчивость филиала;\n• Учёт имущества, обязательств и хозяйственных операций, поступающих основных средств, товарно-материальных ценностей, денежных средств;\n• Начисление и выплата в установленные сроки зарплаты, стипендий, пособий и других выплат;\n• Своевременное проведение расчетов с юридическими и физическими лицами; уплата всех видов налогов и сборов;\n• Ведение учёта федеральных средств, целевых поступлений, доходов и расходов по средствам, полученных от иных источников;\n• ",
        "phone": "8 544 835 47 48",
        "image": "http://localhost:9000/images/5.png"
    },
    {
        "id": 6,
        "name": "Юридический отдел",
        "description": "• осуществление единого исполнения функциональных обязанностей юридической службы в деятельности структурных подразделений Филиала под непосредственным его руководством;\n• обеспечение правовой безопасности образовательной, научной, международной, финансово-хозяйственной и других видов уставной деятельности, осуществляемых Филиалом;\n• методологическое обеспечение правовой работы в деятельности Филиала;\n• организация эффективного использования и учета недвижимого имущества, в том числе путем сдачи его в аренду;",
        "phone": "8 334 515 32 80",
        "image": "http://localhost:9000/images/6.png"
    }
]

draft_order = {
    "id": 123,
    "status": "Черновик",
    "date_created": "12 сентября 2024г",
    "name": "Название приказа",
    "description": "Описание приказа",
    "date": "12 октября 2024г",
    "units": [
        {
            "id": 1,
            "name": "Отдел безопасности и охраны",
            "description": "• Обеспечение надежной защиты объектов филиала от краж, хищений, грабежей, других преступных посягательств и общественных беспорядков;\n• Обеспечение инженерно-технической защиты Филиала;\n• Обеспечение на охраняемых объектах контрольно-пропускного и внутриобъектового режима, предупреждение и пресечение хищений материальных ценностей;\n• Пресечение попыток несанкционированного проникновения на объекты филиала посторонних лиц;\n• Установление порядка допуска сотрудников сторонних организаций, посетителей и транспортных средств на охраняемую территорию;",
            "phone": "8 904 815 31 92",
            "image": "http://localhost:9000/images/1.png",
            "meeting": True
        },
        {
            "id": 2,
            "name": "Ученый совет",
            "description": "• Рассмотрение вопросов текущей деятельности и развития Филиала в целях обеспечения высокого качества подготовки выпускников;\n• Методическое руководство и координация деятельности Филиала в сфере: учебной работы, научно-исследовательской работы, кадровой и административной работы, социальной работы.",
            "phone": "8 914 825 51 52",
            "image": "http://localhost:9000/images/2.png",
            "meeting": False
        },
        {
            "id": 3,
            "name": "Отдел инженерной эксплуатации",
            "description": "• Поддержка учебных корпусов, зданий общежитий в состоянии, обеспечивающем их долголетнюю и надежную работу. Для этого подразделение проводит техническую эксплуатацию зданий, профилактику их конструкций, осуществляет проведение текущего ремонта зданий, поддерживать инженерные системы в учебных корпусах и зданиях общежитий в состоянии, обеспечивающем их долголетнюю и надежную работу.\n• Поддержка электротехнических систем в учебных корпусах и зданиях общежитий в состоянии, обеспечивающем их долголетнюю и надежную работу. Для этого подразделение проводит их техническую эксплуатацию и профилактику конструкций, узлов оборудования и приборов.",
            "phone": "8 753 215 35 11",
            "image": "http://localhost:9000/images/3.png",
            "meeting": True
        },
    ]
}


def getUnitById(unit_id):
    for unit in units:
        if unit["id"] == unit_id:
            return unit


def getUnits():
    return units


def searchUnits(unit_name):
    res = []

    for unit in units:
        if unit_name.lower() in unit["name"].lower():
            res.append(unit)

    return res


def getDraftOrder():
    return draft_order


def getOrderById(order_id):
    return draft_order


def index(request):
    unit_name = request.GET.get("unit_name", "")
    units = searchUnits(unit_name) if unit_name else getUnits()
    draft_order = getDraftOrder()

    context = {
        "units": units,
        "unit_name": unit_name,
        "units_count": len(draft_order["units"]),
        "draft_order": draft_order
    }

    return render(request, "units_page.html", context)


def unit(request, unit_id):
    context = {
        "id": unit_id,
        "unit": getUnitById(unit_id),
    }

    return render(request, "unit_page.html", context)


def order(request, order_id):
    order = getOrderById(order_id)
    units = [
        {**getUnitById(unit["id"]), "meeting": unit["meeting"]}
        for unit in order["units"]
    ]

    context = {
        "order": order,
        "units": units
    }

    return render(request, "order_page.html", context)
