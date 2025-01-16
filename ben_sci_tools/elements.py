

class element:

    def __init__(self,atomic_number:int,symbol:str,name:str,atomic_mass:float):
        
        self.atomic_number = atomic_number
        self.symbol = symbol
        self.name = name.lower().strip()
        self.atomic_mass = atomic_mass
        pass

class periodic_table:

    def __init__(self):
        
        self.elements = [
            element(1,"H","Hydrogen",1.0080),
            element(2,"He","Helium",4.00260),
            element(3,"Li","Lithium",7.0),
            element(4,"Be","Beryllium",9.012183),
            element(5,"B","Boron",10.81),
            element(6,"C","Carbon",12.011),
            element(7,"N","Nitrogen",14.007),
            element(8,"O","Oxygen",15.999),
            element(9,"F","Fluorine",18.99840316),
            element(10,"Ne","Neon",20.180),
            element(11,"Na","Sodium",22.9897693),
            element(12,"Mg","Magnesium",24.305),
            element(13,"Al","Aluminum",26.981538),
            element(14,"Si","Silicon",28.085),
            element(15,"P","Phosphorus",30.97376200),
            element(16,"S","Sulfur",32.07),
            element(17,"Cl","Chlorine",35.45),
            element(18,"Ar","Argon",39.9),
            element(19,"K","Potassium",39.0983),
            element(20,"Ca","Calcium",40.08),
            element(21,"Sc","Scandium",44.95591),
            element(22,"Ti","Titanium",47.867),
            element(23,"V","Vanadium",50.9415),
            element(24,"Cr","Chromium",51.996),
            element(25,"Mn","Manganese",54.93804),
            element(26,"Fe","Iron",55.84),
            element(27,"Co","Cobalt",58.93319),
            element(28,"Ni","Nickel",58.693),
            element(29,"Cu","Copper",63.55),
            element(30,"Zn","Zinc",65.4),
            element(31,"Ga","Gallium",69.723),
            element(32,"Ge","Germanium",72.63),
            element(33,"As","Arsenic",74.92159),
            element(34,"Se","Selenium",78.97),
            element(35,"Br","Bromine",79.90),
            element(36,"Kr","Krypton",83.80),
            element(37,"Rb","Rubidium",85.468),
            element(38,"Sr","Strontium",87.62),
            element(39,"Y","Yttrium",88.90584),
            element(40,"Zr","Zirconium",91.22),
            element(41,"Nb","Niobium",92.90637),
            element(42,"Mo","Molybdenum",95.95),
            element(43,"Tc","Technetium",96.90636),
            element(44,"Ru","Ruthenium",101.1),
            element(45,"Rh","Rhodium",102.9055),
            element(46,"Pd","Palladium",106.42),
            element(47,"Ag","Silver",107.868),
            element(48,"Cd","Cadmium",112.41),
            element(49,"In","Indium",114.818),
            element(50,"Sn","Tin",118.71),
            element(51,"Sb","Antimony",121.760),
            element(52,"Te","Tellurium",127.6),
            element(53,"I","Iodine",126.9045),
            element(54,"Xe","Xenon",131.29),
            element(55,"Cs","Cesium",132.9054520),
            element(56,"Ba","Barium",137.33),
            element(57,"La","Lanthanum",138.9055),
            element(58,"Ce","Cerium",140.116),
            element(59,"Pr","Praseodymium",140.90766),
            element(60,"Nd","Neodymium",144.24),
            element(61,"Pm","Promethium",144.91276),
            element(62,"Sm","Samarium",150.4),
            element(63,"Eu","Europium",151.964),
            element(64,"Gd","Gadolinium",157.25),
            element(65,"Tb","Terbium",158.92535),
            element(66,"Dy","Dysprosium",162.500),
            element(67,"Ho","Holmium",164.93033),
            element(68,"Er","Erbium",167.26),
            element(69,"Tm","Thulium",168.93422),
            element(70,"Yb","Ytterbium",173.05),
            element(71,"Lu","Lutetium",174.9667),
            element(72,"Hf","Hafnium",178.49),
            element(73,"Ta","Tantalum",180.9479),
            element(74,"W","Tungsten",183.84),
            element(75,"Re","Rhenium",186.207),
            element(76,"Os","Osmium",190.2),
            element(77,"Ir","Iridium",192.22),
            element(78,"Pt","Platinum",195.08),
            element(79,"Au","Gold",196.96657),
            element(80,"Hg","Mercury",200.59),
            element(81,"Tl","Thallium",204.383),
            element(82,"Pb","Lead",207),
            element(83,"Bi","Bismuth",208.98040),
            element(84,"Po","Polonium",208.98243),
            element(85,"At","Astatine",209.98715),
            element(86,"Rn","Radon",222.01758),
            element(87,"Fr","Francium",223.01973),
            element(88,"Ra","Radium",226.02541),
            element(89,"Ac","Actinium",227.02775),
            element(90,"Th","Thorium",232.038),
            element(91,"Pa","Protactinium",231.03588),
            element(92,"U","Uranium",238.0289),
            element(93,"Np","Neptunium",237.048172),
            element(94,"Pu","Plutonium",244.06420),
            element(95,"Am","Americium",243.061380),
            element(96,"Cm","Curium",247.07035),
            element(97,"Bk","Berkelium",247.07031),
            element(98,"Cf","Californium",251.07959),
            element(99,"Es","Einsteinium",252.0830),
            element(100,"Fm","Fermium",257.09511),
            element(101,"Md","Mendelevium",258.09843),
            element(102,"No","Nobelium",259.10100),
            element(103,"Lr","Lawrencium",266.120),
            element(104,"Rf","Rutherfordium",267.122),
            element(105,"Db","Dubnium",268.126),
            element(106,"Sg","Seaborgium",269.128),
            element(107,"Bh","Bohrium",270.133),
            element(108,"Hs","Hassium",269.1336),
            element(109,"Mt","Meitnerium",277.154),
            element(110,"Ds","Darmstadtium",282.166),
            element(111,"Rg","Roentgenium",282.169),
            element(112,"Cn","Copernicium",286.179),
            element(113,"Nh","Nihonium",286.182),
            element(114,"Fl","Flerovium",290.192),
            element(115,"Mc","Moscovium",290.196),
            element(116,"Lv","Livermorium",293.205),
            element(117,"Ts","Tennessine",294.211),
            element(118,"Og","Oganesson",295.216),
        ]
        pass


    def element_by_number(self,atomic_number:int):
        for e in self.elements:
            if e.atomic_number == atomic_number:
                return e
        return None
    
    def element_by_name(self,name:str):
        comp = name.lower().strip()
        for e in self.elements:
            if e.name == comp:
                return e
        return None
    
    def element_by_symbol(self,symbol:str):
        comp = symbol.strip()
        for e in self.elements:
            if e.symbol == comp:
                return e
        return None