from copy import deepcopy
import flet
from metodo_cesar import cifrado_cesar, descifrado_cesar
from parametros import codigo_desde_matriz_generadora


from flet import (
    AppBar,
    Card,
    Column,
    Container,
    Divider,
    ElevatedButton,
    IconButton,
    Icon,
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
            # bgcolor=colors.SURFACE_VARIANT,
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
            bgcolor=colors.SURFACE_VARIANT,
            toolbar_height=48,

        )
        

        appbar.actions = [
            Row(
                [   
                    title := Text("Code Genius", weight="bold"),
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
                            padding=10
                        )),
                    Row(
                        controls=[
                            tf_clave,
                            tf_cifrado,
                            
                        ],
                    ),
                    texto,
                    Text(body),
                    Card(content=Container(
                        Text(title2, weight="bold"), 
                        padding=8
                        )),
                    Row(
                        #* Centrarlo bien :)
                        controls=[
                            tf_clave2,
                            tf_cifrado2,
                        ],
                    ),
                    texto2,
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
    
def create_page_cl(title: str, body: str, page):
    tf_cl = TextField(label="Ingrese el código lineal")
    tf_p = TextField(label="Ingrese el valor del orden del cuerpo")
    bttn_cl = ElevatedButton(text="Calcular", on_click=lambda e: calcular_cl(tf_cl, tf_p, page))
    tf_salida_cl = TextField(label="Resultado", multiline=True, disabled=True)
    
    return Row(
        controls=[
            Column(
                horizontal_alignment="stretch",
                controls=[
                    Card(content=Container(
                        Text(title, weight="bold"), 
                        padding=8
                        )),
                    Text("Ingrese el código lineal y el valor del orden del cuerpo para calcular el resultado."),
                    Text("Un ejemplo de cómo introducir un código lineal es: [[0,0,0],[1,1,1],[1,0,0], [0,1,1]]"),
                    tf_cl,
                    Row(
                        #* Centrarlo bien :)
                        controls=[
                            tf_p,
                            bttn_cl,
                        ],
                    ),
                    Text(body),
                    tf_salida_cl,
                ],
                expand=True,
            ),
        ],
        expand=True,
    )
    
def create_page_mg(title: str, body: str, page):
    tf_mg = TextField(label="   Ingrese la matriz generadora")
    bttn_mg = ElevatedButton(text="Calcular", on_click=lambda e: calcular_mg(tf_mg, tf_par , page))
    tf_par = TextField(label="Resultado", multiline=True, read_only=True)
    return Row(
        controls=[
            Column(
                horizontal_alignment="stretch",
                controls=[
                    Card(content=Container(
                        Text(title, weight="bold"), 
                        padding=8
                        )),
                    Text("   Ingrese la matriz generadora para calcular el resultado."),
                    Text("   Un ejemplo de cómo introducir la matriz generadora es: [[1,0,0], [0,1,1]]"),
                    tf_mg,
                    Row(
                        #* Centrarlo bien :)
                        controls=[
                            bttn_mg,
                        ],
                    ),
                    Text(body),
                    tf_par,
                ],
                expand=True,
            ),
        ],
        expand=True,
    )

def create_page_cd(title: str, body: str, page):
    tf_cd = TextField(label="   Ingrese el código lineal")
    bttn_cd = ElevatedButton(text="Calcular", on_click=lambda e: calcular_cd(tf_cd, page))
    tf_rcd = TextField(label=" Código Dual", multiline=True, disabled=True)
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
                    Text("   Un ejemplo de cómo introducir un código lineal es: [[0,0,0],[1,1,1],[1,0,0], [0,1,1]]"),
                    tf_cd,
                    bttn_cd,
                    Text(body),
                    tf_rcd,
                ],
                expand=True,
            ),
        ],
        expand=True,
        
    )
    

def calcular_mg(tf_mg, tf_r, page):
    tf_r.value = ""
    valor = tf_mg.value
    convertir_numero = lambda x: int("".join(filter(str.isdigit, x)))
    vectorizar = [[convertir_numero(i) for i in j.split(",")] for j in valor.split("], [")]
    resultado = codigo_desde_matriz_generadora(vectorizar)
    tf_r.value = f"Longitud del código: {resultado[0]}\nDimensión del código: {resultado[1]}\nDistancia mínima del código: {resultado[2]}\nCardinalidad del código: {resultado[3]}"
    page.update()
    
def calcular_cl(tf_cl, tf_p, page):
    pass



def calcular_cd(tf_cd, page):
    pass
    

def main(page: Page):
    pages = [
        (
            NavigationRailDestination(
                icon=icons.LANDSCAPE_OUTLINED,
                selected_icon=icons.LANDSCAPE,
                label="Cifrado César",
            ),
            create_page_cifrado(" Cifrado César", "Para actualizar el cifrado, actualiza el texto a cifrar.", "DesCifrado César", page),
        ),
        (
            NavigationRailDestination(
                icon=icons.PORTRAIT_OUTLINED,
                selected_icon=icons.PORTRAIT,
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
                icon=icons.INSERT_EMOTICON_OUTLINED,
                selected_icon=icons.INSERT_EMOTICON,
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
                icon=icons.INSERT_EMOTICON_OUTLINED,
                selected_icon=icons.INSERT_EMOTICON,
                label="Código Dual",
            ),
            create_page_cd(
                " Código Lineal a Dual",
                "   This is an example page. It is a simple desktop layout with a menu on the left.",
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



if __name__ == "__main__":
    flet.app(
        target=main,
    )
    
    