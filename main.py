from copy import deepcopy
import flet
from metodo_cesar import cifrado_cesar, descifrado_cesar
from parametros import analisis_codigo_lineal
from punto2 import matriz_generadora
from Punto4 import codigo_dual, matriz_control

from flet import (
    AppBar,
    Card,
    Column,
    Container,
    Divider,
    ElevatedButton,
    IconButton,
    Icon,
    Image,
    NavigationRail,
    NavigationRailDestination,
    Page,
    PopupMenuButton,
    PopupMenuItem,
    Row,
    Text,    
    TextField,
    margin,
    alignment,
    padding
)
from flet import colors, icons


class DesktopAppLayout(Row):
    """A desktop app layout with a menu on the left."""

    def __init__(
        self,
        title,
        page,
        pages,
        *args,
        window_size=(800, 600),
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.page = page
        self.pages = pages

        self.expand = True

        self.navigation_items = [navigation_item for navigation_item, _ in pages]
        self.navigation_rail = self.build_navigation_rail()
        self.update_destinations()
        self._menu_extended = True
        self.navigation_rail.extended = True

        self.menu_panel = Row(
            alignment="left",
            vertical_alignment="top",
            controls=[
                self.navigation_rail,
            ],
            spacing=0,
            tight=True,
        )

        page_contents = [page_content for _, page_content in pages]
        self.content_area = Column(page_contents, expand=True)

        self._was_portrait = self.is_portrait()
        self._panel_visible = self.is_landscape()

        self.set_content()

        self._change_displayed_page()

        self.page.on_resize = self.handle_resize

        self.page.appbar = self.create_appbar()
        

        self.window_size = window_size
        self.page.window_width, self.page.window_height = self.window_size

        self.page.title = title

    def select_page(self, page_number):
        self.navigation_rail.selected_index = page_number
        self._change_displayed_page()

    def _navigation_change(self, e):
        self._change_displayed_page()
        self.page.update()

    def _change_displayed_page(self):
        page_number = self.navigation_rail.selected_index
        for i, content_page in enumerate(self.content_area.controls):
            # update selected page
            content_page.visible = page_number == i

    def build_navigation_rail(self):
        return NavigationRail(
            selected_index=0,
            label_type="none",
            on_change=self._navigation_change,
        )

    def update_destinations(self):
        self.navigation_rail.destinations = self.navigation_items
        self.navigation_rail.label_type = "all"

    def handle_resize(self, e):
        pass

    def set_content(self):
        self.controls = [self.menu_panel, self.content_area]
        self.update_destinations()
        self.navigation_rail.extended = self._menu_extended
        self.menu_panel.visible = self._panel_visible

    def is_portrait(self) -> bool:
        # Return true if window/display is narrow
        # return self.page.window_height >= self.page.window_width
        return self.page.height >= self.page.width

    def is_landscape(self) -> bool:
        # Return true if window/display is wide
        return self.page.width > self.page.height

    def create_appbar(self) -> AppBar:
        appbar = AppBar(
            toolbar_height=48,
            elevation=4,
        )
        

        appbar.actions = [
            Row(
                [   
                    title := Text("Code Genius", size=22, color=colors.ON_PRIMARY_CONTAINER, font_family="Constantia", text_align="center"),
                    PopupMenuButton(
                        icon=icons.PERSON,
                        items=[
                            PopupMenuItem(
                                text="Presentado por:",
                            ),
                            PopupMenuItem(
                                icon=icons.PERSON_OUTLINED,
                                text="Samuel Matiz",
                            ),
                            PopupMenuItem(
                                icon=icons.PERSON_2_SHARP,
                                text="Camilo Navarro",
                            ),
                            PopupMenuItem(
                                icon=icons.PERSON_3_OUTLINED,
                                text="María C. Osorno",
                            ),
                            PopupMenuItem(
                                icon=icons.PERSON_ROUNDED,
                                text="Alberto Sandoval",
                            ),
                            PopupMenuItem(
                                icon=icons.PERSON_2_OUTLINED,
                                text="Juan F. Santos",
                            ),
                        ],
                        
                    )
                ]
            )
        ]
        return appbar


def create_page(title: str, body: str):
    return Row(
        controls=[
            Column(
                horizontal_alignment="stretch",
                controls=[
                    Card(content=Container(Text(title, weight="bold"), padding=8)),
                    Text(body),
                ],
                expand=True,
            ),
        ],
        expand=True,
    )

def create_page_cifrado(title: str, body: str, title2:str, page):
    tf_clave = TextField(label="Ingrese la clave de cifrado", keyboard_type="NUMBER", value="0", )
    texto = Text("Texto cifrado: ")
    tf_cifrado = TextField(label="Ingrese la frase a cifrar", on_change=lambda e: cifrado(texto, tf_cifrado, tf_clave.value, page))
    tf_clave2 = TextField(label="Ingrese la clave de descifrado", keyboard_type="NUMBER", value="0")
    texto2 = Text("Texto descifrado: ")
    tf_cifrado2 = TextField(label="Ingrese la frase cifrada", on_change=lambda e: descifrado(texto2, tf_cifrado2, tf_clave2.value, page))

    
    return Row(
        controls=[
            Column(
                horizontal_alignment="stretch",
                controls=[
                    Card(content=
                        Container(
                            Text(title, weight="bold" ), 
                            padding=12
                        )),
                    Card(content=Container( 
                        Text(value = "El cifrado César es una técnica de criptografía clásica que se basa en desplazar cada letra de un texto una cantidad fija de posiciones en el alfabeto. Por ejemplo, con un desplazamiento de 3, la letra A se convertiría en D, la B en E y así sucesivamente."),
                        padding=12,
                    ),
                    ),
                    Divider(),
                    Row(
                        controls=[
                            Container(
                                tf_clave,
                                padding=12,
                            ),
                            Container(
                                tf_cifrado,
                                padding=12,
                            )
                        ],
                    ),
                    Divider(),
                    texto,
                    Text(body),
                    Card(content=Container(
                        Text(title2, weight="bold"), 
                        padding=12
                        )),
                    Row(
                        controls=[
                            Container(
                                tf_clave2,
                                padding = 12,
                            ),
                            Container(
                                tf_cifrado2,
                                padding = 12,
                            ),
                        ],
                    ),
                    texto2,
                    Divider(),
                ],
                expand=True,
            ),
        ],
        expand=True,
    )

def cifrado(campo_texto, textf, clave:int, page):
    campo_texto.value = f"Texto cifrado: {cifrado_cesar(textf.value, int(clave))}"
    page.update()
    
def descifrado(campo_texto, textf, clave:int, page):
    campo_texto.value = f"Texto descifrado: {descifrado_cesar(textf.value, int(clave))}"
    page.update()
    
def calcular_mg(tf_mg, tf_r, tf_mgp, page):
    tf_r.value = ""
    valor = tf_mg.value
    convertir_numero = lambda x: int("".join(filter(str.isdigit, x)))
    vectorizar = [[convertir_numero(i) for i in j.split(",")] for j in valor.split("], [")]
    resultado = analisis_codigo_lineal(vectorizar, int(tf_mgp.value))
    tf_r.value = resultado
    page.update()
    
def calcular_cl(tf_cl, tf_p, tf_salida,  page):
    tf_salida.value = ""
    valor = tf_cl.value
    convertir_numero = lambda x: int("".join(filter(str.isdigit, x)))
    vectorizar = [[convertir_numero(i) for i in j.split(",")] for j in valor.split("], [")]
    resultado = matriz_generadora(vectorizar, int(tf_p.value))
    tf_salida.value = resultado
    page.update()
    
def ejemploCL(tf_cl, tf_p, page, num):
    tf_cl.value = ""
    tf_p.value = ""
    if num == 1:
        tf_cl.value = "[[1,0], [1,1], [0,1], [0,0]]"
        tf_p.value = "2"
    elif num == 2:
        tf_cl.value = "[[1,0,1], [0,0,1], [1,0,0], [0,0,0]]"
        tf_p.value = "2"
    elif num == 3:
        tf_cl.value = "[[0,0,0,0], [1,1,0,0], [0,0,1,1], [1,1,1,1]]"
        tf_p.value = "2"
    elif num == 4:
        tf_cl.value = "[[2,1,2,3,4], [4,2,4,1,3], [1,3,1,4,2], [3,4,3,2,1], [0,0,0,0,0]]"
        tf_p.value = "5"
    elif num == 5:
        tf_cl.value = "[[0,1,0,0], [1,1,0,1], [1,0,1,0], [1,0,0,1], [1,1,1,0], [0,1,1,1], [0,0,1,1], [0,0,0,0]]"
        tf_p.value = "2"
        
    page.update()
    
def create_page_cl(title: str, body: str, page):
    tf_cl = TextField(label="Ingrese el código lineal")
    tf_p = TextField(label="Ingrese el valor del orden del cuerpo")
    bttn_cl = ElevatedButton(text="Calcular", on_click=lambda e: calcular_cl(tf_cl, tf_p, tf_salida_cl, page))
    tf_salida_cl = TextField(label="Resultado", multiline=True, read_only=True)
    bttn_ej1CL = ElevatedButton(text="Ejemplo 1", on_click=lambda e: ejemploCL(tf_cl, tf_p, page, 1))
    bttn_ej2CL = ElevatedButton(text="Ejemplo 2", on_click=lambda e: ejemploCL(tf_cl, tf_p, page, 2))
    bttn_ej3CL = ElevatedButton(text="Ejemplo 3", on_click=lambda e: ejemploCL(tf_cl, tf_p, page, 3))
    bttn_ej4CL = ElevatedButton(text="Ejemplo 4", on_click=lambda e: ejemploCL(tf_cl, tf_p, page, 4))
    bttn_ej5CL = ElevatedButton(text="Ejemplo 5", on_click=lambda e: ejemploCL(tf_cl, tf_p, page, 5))
    
    return Row(
        controls=[
            Column(
                horizontal_alignment="stretch",
                controls=[
                    Card(content=Container(
                        Text(title, weight="bold"), 
                        padding=8
                        )),
                    Container(
                        Text("Un código lineal es un subespacio de un espacio vectorial finito que se define mediante un conjunto de vectores linealmente independientes. \n Ingresa el código lineal y el valor del orden del cuerpo para calcular el resultado.\nUn ejemplo de cómo introducir un código lineal es: [[0,0,0], [1,1,1], [1,0,0], [0,1,1]]"),
                        padding=12,
                    ),
                    Container(
                        tf_cl,
                        padding=12,
                    ),
                    Row(
                        controls=[
                            Container(
                                tf_p,
                                padding=12,
                            ),
                            Container(
                                bttn_cl,
                                padding=12,
                            ),
                        ],
                    ),
                    Divider(),
                    Container(
                        Text(body),
                        padding=12,
                    ),
                    Container(
                        tf_salida_cl,
                        padding=12,
                    ),
                    Divider(),
                    Card(content=Container(
                        Text("Ejemplos Sugeridos", weight="bold"), 
                        padding=8
                        )),
                    Row
                    (
                        controls=[
                            bttn_ej1CL,
                            bttn_ej2CL,
                            bttn_ej3CL,
                            bttn_ej4CL,
                            bttn_ej5CL,
                        ],
                        alignment="center",
                        
                    ),
                ],
                expand=True,
            ),
        ],
        expand=True,
    )
    
def ejemploMG(tf_mg, tf_par, page, num):
    tf_mg.value = ""
    if num == 1:
        tf_mg.value = "[[1,0,0,0], [0,1,0,0], [0,0,1,0]]"
        tf_par.value = "2"
    elif num == 2:
        tf_mg.value = "[[1,1,0,0], [0,1,1,0], [0,0,1,1]]"
        tf_par.value = "2"
    elif num == 3:
        tf_mg.value = "[[1,1,1,1,1]]"
        tf_par.value = "2"
    elif num == 4:
        tf_mg.value = "[[1,0,0,0], [0,1,0,0], [0,0,1,1]]"
        tf_par.value = "2"
    elif num == 5:
        tf_mg.value = "[[1,1,1,0,0], [0,0,1,1,1]]"
        tf_par.value = "2"
        
    page.update()

def create_page_mg(title: str, body: str, page):
    tf_mg = TextField(label="   Ingrese la matriz generadora")
    tf_mgp = TextField(label="Ingrese el valor del orden del cuerpo")
    bttn_mg = ElevatedButton(text="Calcular", on_click=lambda e: calcular_mg(tf_mg, tf_par , tf_mgp, page))
    tf_par = TextField(label="Resultado", multiline=True, read_only=True)
    bttn_ej1MG = ElevatedButton(text="Ejemplo 1", on_click=lambda e: ejemploMG(tf_mg, tf_mgp, page, 1))
    bttn_ej2MG = ElevatedButton(text="Ejemplo 2", on_click=lambda e: ejemploMG(tf_mg, tf_mgp, page, 2))
    bttn_ej3MG = ElevatedButton(text="Ejemplo 3", on_click=lambda e: ejemploMG(tf_mg, tf_mgp, page, 3))
    bttn_ej4MG = ElevatedButton(text="Ejemplo 4", on_click=lambda e: ejemploMG(tf_mg, tf_mgp, page, 4))
    bttn_ej5MG = ElevatedButton(text="Ejemplo 5", on_click=lambda e: ejemploMG(tf_mg, tf_mgp, page, 5))
    return Row(
        controls=[
            Column(
                horizontal_alignment="stretch",
                controls=[
                    Card(content=Container(
                        Text(title, weight="bold"), 
                        padding=8
                        )),
                    Container(
                        Text(" Ingrese la matriz generadora para calcular el resultado. \n Un ejemplo de cómo introducir una matriz generadora es: [[1,0,0,0], [0,1,0,0], [0,0,1,0]]"),
                        padding=12,
                    ),
                    Divider(),
                    Row(
                        controls=[
                            Container(
                                tf_mg,
                                padding=12,
                            ),
                            Row(
                                controls=[
                                    Container(
                                        tf_mgp,
                                        padding=12,
                                    ),
                                    Container(
                                        bttn_mg,
                                        padding=12,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Container(
                        Text(body),
                        padding=12,
                    ),
                    Container(
                        tf_par,
                        padding=12,
                    ),
                    Divider(),
                    Card(content=Container(
                        Text("Ejemplos Sugeridos", weight="bold"), 
                        padding=8
                        )),
                    Row
                    (
                        controls=[
                            bttn_ej1MG,
                            bttn_ej2MG,
                            bttn_ej3MG,
                            bttn_ej4MG,
                            bttn_ej5MG,
                        ],
                        alignment="center",
                        
                    ),
                ],
                expand=True,
            ),
        ],
        expand=True,
    )

def calcular_cd(tf_cd, tf_cdp, tf_rcd, page):
    tf_rcd.value = ""
    valor = tf_cd.value
    convertir_numero = lambda x: int("".join(filter(str.isdigit, x)))
    vectorizar = [[convertir_numero(i) for i in j.split(",")] for j in valor.split("], [")]
    resultado = codigo_dual(vectorizar, int(tf_cdp.value))
    tf_rcd.value = resultado
    page.update()

def ejemploCD(tf_cd, tf_cdp, page, num):
    tf_cd.value = ""
    tf_cdp.value = ""
    if num == 1:
        tf_cd.value = "[[0,0,0,0,0], [0,1,1,1,1], [1,0,0,1,0], [1,1,1,0,1]]"
        tf_cdp.value = "2"
    elif num == 2:
        tf_cd.value = "[[0,0,0], [0,1,1], [1,0,1], [1,1,0]]"
        tf_cdp.value = "2"
    elif num == 3:
        tf_cd.value = "[[0,0,0,0,0,0,0], [0,0,0,1,0,1,1], [0,0,1,0,1,0,1], [0,0,1,1,1,1,0], [0,1,0,0,1,1,0], [0,1,0,1,1,0,1], [0,1,1,0,0,1,1], [0,1,1,1,0,0,0], [1,0,0,0,1,1,1], [1,0,0,1,1,0,0], [1,0,1,0,0,1,0], [1,0,1,1,0,0,1], [1,1,0,0,0,0,1], [1,1,0,1,0,1,0], [1,1,1,0,1,0,0], [1,1,1,1,1,1,1]]"
        tf_cdp.value = "2"
    elif num == 4:
        tf_cd.value = "[[0,0,0,0,0,0], [1,1,1,0,0,0], [0,0,0,1,1,1], [1,1,1,1,1,1]]"
        tf_cdp.value = "2"
    elif num == 5:
        tf_cd.value = "[[0,0,0,0], [1,2,0,1], [2,1,0,2], [1,1,1,0], [2,0,1,1], [0,2,1,2], [2,2,2,0], [0,1,2,1], [1,0,2,2]]"
        tf_cdp.value = "3"
        
    page.update()

def create_page_cd(title: str, body: str, page):
    tf_cd = TextField(label="   Ingrese el código lineal", multiline=True)
    tf_cdp = TextField(label="Ingrese el valor del orden del cuerpo")
    tf_rcd = TextField(label=" Código Dual", multiline=True, read_only=True)
    bttn_cd = ElevatedButton(text="Calcular", on_click=lambda e: calcular_cd(tf_cd, tf_cdp, tf_rcd, page))
    bttn_ej1CD = ElevatedButton(text="Ejemplo 1", on_click=lambda e: ejemploCD(tf_cd, tf_cdp, page, 1))
    bttn_ej2CD = ElevatedButton(text="Ejemplo 2", on_click=lambda e: ejemploCD(tf_cd, tf_cdp, page, 2))
    bttn_ej3CD = ElevatedButton(text="Ejemplo 3", on_click=lambda e: ejemploCD(tf_cd, tf_cdp, page, 3))
    bttn_ej4CD = ElevatedButton(text="Ejemplo 4", on_click=lambda e: ejemploCD(tf_cd, tf_cdp, page, 4))
    bttn_ej5CD = ElevatedButton(text="Ejemplo 5", on_click=lambda e: ejemploCD(tf_cd, tf_cdp, page, 5))
    
    return Row(
        controls=[
            Column(
                horizontal_alignment="stretch",
                controls=[
                    Card(content=Container(
                        Text(title, weight="bold"), 
                        padding=8
                        )),
                    Text("   Ingrese el código lineal para calcular el código dual."),
                    Text("   Un ejemplo de cómo introducir un código lineal es: [[0,0,0], [1,1,1], [1,0,0], [0,1,1]]"),
                    Container(
                        tf_cd,
                        padding=12,
                    ),
                    Row(
                        controls=[
                            Container(
                                tf_cdp,
                                padding=12,
                            ),
                            Container(
                                bttn_cd,
                                padding=12,
                            ),
                        ],
                    ),
                    Divider(),
                    Container(
                        Text(body),
                        padding=12,
                    ),
                    Container(
                        tf_rcd,
                        padding=12,
                    ),
                    Divider(),
                    Card(content=Container(
                        Text("Ejemplos Sugeridos", weight="bold"), 
                        padding=8
                        )),
                    Row
                    (
                        controls=[
                            bttn_ej1CD,
                            bttn_ej2CD,
                            bttn_ej3CD,
                            bttn_ej4CD,
                            bttn_ej5CD,
                        ],
                        alignment="center",
                        
                    ),
                ],
                expand=True,
            ),
        ],
        expand=True,
    
    )

def create_page_inicio(title: str, body: str, title2:str, page):
    logo = Image(
        src="./assets/codeg_logo.png",
        width=500,
        height=500, 
    )
    return Column(
        horizontal_alignment="stretch",
        controls=[
            Card(content=Container(
                Text(title, weight="bold", text_align="center", size=24, font_family="Constantia"), 
                padding=10,
                ),
                 color=colors.BACKGROUND,
                 margin=20,
                elevation=5),
            logo,
            Divider(),
            Text(body, text_align="center"),
        ],
        
    )
    
def ejemploMC(tf_mg, tf_pmc,  page, num):
    if num == 1:
        tf_mg.value = "[[1,0,0], [0,1,1]]"
        tf_pmc.value = "2"
    elif num == 2:
        tf_mg.value = "[[1,0,1,0,1], [0,1,1,1,0]]"
        tf_pmc.value = "2"
    elif num == 3:
        tf_mg.value = "[[1,0,0,0,1,1,1], [0,1,0,0,1,1,0], [0,0,1,0,1,0,1], [0,0,0,1,0,1,1]]"
        tf_pmc.value = "2"
    elif num == 4:
        tf_mg.value = "[[1,0,1,2], [0,1,2,2]]"
        tf_pmc.value = "3"
    elif num == 5:
        tf_mg.value = "[[1,1,1,0], [0,0,0,1]]"
        tf_pmc.value = "2"
    page.update()

def calcular_mc(tf_mg, tf_salida, tf_pmc, page):
    tf_salida.value = ""
    valor = tf_mg.value
    convertir_numero = lambda x: int("".join(filter(str.isdigit, x)))
    vectorizar = [[convertir_numero(i) for i in j.split(",")] for j in valor.split("], [")]
    resultado = matriz_control(vectorizar, int(tf_pmc.value))
    tf_salida.value = resultado
    page.update()

def create_page_mc(title: str, body: str, page):
    tf_mg = TextField(label="   Ingrese la matriz generadora", multiline=True)
    tf_pmc = TextField(label="Ingrese el valor del orden del cuerpo")
    tf_par = TextField(label="Resultado", multiline=True, read_only=True)
    bttn_mg = ElevatedButton(text="Calcular", on_click=lambda e: calcular_mc(tf_mg, tf_par, tf_pmc, page))
    bttn_ej1MG = ElevatedButton(text="Ejemplo 1", on_click=lambda e: ejemploMC(tf_mg, tf_pmc, page, 1))
    bttn_ej2MG = ElevatedButton(text="Ejemplo 2", on_click=lambda e: ejemploMC(tf_mg, tf_pmc, page, 2))
    bttn_ej3MG = ElevatedButton(text="Ejemplo 3", on_click=lambda e: ejemploMC(tf_mg, tf_pmc, page, 3))
    bttn_ej4MG = ElevatedButton(text="Ejemplo 4", on_click=lambda e: ejemploMC(tf_mg, tf_pmc, page, 4))
    bttn_ej5MG = ElevatedButton(text="Ejemplo 5", on_click=lambda e: ejemploMC(tf_mg, tf_pmc, page, 5))
    
    return Row(
        controls=[
            Column(
                horizontal_alignment="stretch",
                controls=[
                    Card(content=Container(
                        Text(title, weight="bold"), 
                        padding=8
                        )),
                    Container(
                        Text("Una matriz de control es una herramienta fundamental en teoría de códigos que facilita el diseño, análisis y optimización de códigos para su aplicación en sistemas de comunicación, almacenamiento y transmisión de información."),
                        padding=12,
                    ),
                    Divider(),
                    Row(
                        controls=[
                            Container(
                                tf_mg,
                                padding = 12,
                            ),
                            Container(
                                tf_pmc,
                                padding = 12,
                            ),
                            bttn_mg,
                        ],
                    ),
                    Divider(),
                    Text(body),
                    Container(
                        tf_par,
                        padding=12,
                    ),
                    Divider(),
                    Card(content=Container(
                        Text("Ejemplos Sugeridos", weight="bold"), 
                        padding=8
                        )),
                    
                    Row(
                        alignment="center",
                        controls=[
                            bttn_ej1MG,
                            bttn_ej2MG,
                            bttn_ej3MG,
                            bttn_ej4MG,
                            bttn_ej5MG,
                        ],
                    ),
                ],
                expand=True,
            ),
        ],
        expand=True,
    )

def main(page: Page):
    pages = [
        (
            NavigationRailDestination(
                icon=icons.HOME_ROUNDED,
                selected_icon=icons.HOME_ROUNDED,
                label="Inicio",
            ),
            create_page_inicio(" Bienvenid@ a Code Genius", "Seleccione cualquier item del menú para comenzar", "DesCifrado César", page),
        ),
        (
            NavigationRailDestination(
                icon=icons.FITBIT_OUTLINED,
                selected_icon=icons.FITBIT_OUTLINED,
                label="Cifrado César",
            ),
            create_page_cifrado(" Cifrado César", "Para actualizar el cifrado, actualiza el texto a cifrar.", "DesCifrado César", page),
        ),
        (
            NavigationRailDestination(
                icon=icons.SETTINGS_OVERSCAN_ROUNDED,
                selected_icon=icons.SETTINGS_OVERSCAN_ROUNDED,
                label="CL a MG",
            ),
            create_page_cl(
                " Código Lineal a Matriz Generadora",
                "   Aquí obtenemos la matriz generadora.",
                page
            ),
        ),
        (
            NavigationRailDestination(
                icon=icons.CONTROL_POINT_DUPLICATE_ROUNDED,
                selected_icon=icons.CONTROL_POINT_DUPLICATE_ROUNDED,
                label="Matriz Control",
            ),
            create_page_mc(" Matriz de Control", "Aquí obtenemos la matriz de control", page),
        ),
        (
            NavigationRailDestination(
                icon=icons.ACCOUNT_TREE_OUTLINED,
                selected_icon=icons.ACCOUNT_TREE_OUTLINED,
                label="Parámetros CL",
            ),
            create_page_mg(
                " Matriz Generadora a Parámetros del Código",
                "   Ojo, entre cambio de fila agrega un espacio como en el ejemplo. Aquí obtenemos los parámetros del código lineal.",
                page
            ),
        ),
        (
            NavigationRailDestination(
                icon=icons.CODE_ROUNDED,
                selected_icon=icons.CODE_ROUNDED,
                label="Código Dual",
            ),
            create_page_cd(
                " Código Lineal a Dual",
                "   Aquí obtenemos el código dual.",
                page
            ),
        )
    ]

    menu_layout = DesktopAppLayout(
        page=page,
        pages=pages,
        title="Code Genius",
        window_size=(1280, 720),
    )

    page.add(menu_layout)
    page.theme_mode = flet.ThemeMode.LIGHT
    page.theme = flet.Theme(
        color_scheme_seed=colors.YELLOW,
    )
    page.bgcolor = "#fffdf7"
    page.appbar.bgcolor = colors.SECONDARY_CONTAINER
    page.update()
    
    
    
    



if __name__ == "__main__":
    flet.app(
        target=main,
    )
    

