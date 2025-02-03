import pandas as pd
import random
import time  
import csv   
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.clock import Clock
from kivy.properties import StringProperty




Window.clearcolor = (1, 1, 1, 1)  


BUTTON_COLOR = (0.0, 0.8, 0.0, 1) 


default_independencia_preguntas = [
    {
        'question': '¿En qué fecha se declaró la independencia de Colombia?',
        'options': ['20 de julio de 1810', '7 de agosto de 1819',
                    '12 de octubre de 1492', '5 de julio de 1811'],
        'correct_answer': 'A'
    },
    
]

default_boyaca_preguntas = [
    {
        'question': '¿En qué año ocurrió la Batalla de Boyacá?',
        'options': ['1810', '1819', '1821', '1824'],
        'correct_answer': 'B'
    },

]

default_guerra_preguntas = [
    {
        'question': '¿Cuándo inició la Guerra de los Mil Días?',
        'options': ['1899', '1902', '1910', '1886'],
        'correct_answer': 'A'
    },
    
]

def cargar_preguntas(archivo_csv, default_questions):
    preguntas = []
    try:
        df = pd.read_csv(archivo_csv)
        print(f"Cargando preguntas desde {archivo_csv}")
        print(f"Columnas encontradas: {df.columns.tolist()}")
        for _, row in df.iterrows():
            preguntas.append({
                'question': str(row['Pregunta']),
                'options': [str(row['Opción_A']), str(row['Opción_B']),
                            str(row['Opción_C']), str(row['Opción_D'])],
                'correct_answer': str(row['Respuesta_Correcta']).strip().upper()
            })
        if not preguntas:
            raise ValueError("No se encontraron preguntas en el archivo CSV.")
        print(f"Total de preguntas cargadas: {len(preguntas)}")
    except (FileNotFoundError, KeyError, ValueError, pd.errors.EmptyDataError) as e:
        print(f"Error al cargar {archivo_csv}: {e}")
        print("Usando preguntas predeterminadas.")
        preguntas = default_questions
    return preguntas



independencia_preguntas = cargar_preguntas('preguntas idependencia.csv',
                                           default_independencia_preguntas)
boyaca_preguntas = cargar_preguntas('preguntas bataya.csv',
                                    default_boyaca_preguntas)
guerra_preguntas = cargar_preguntas('preguntas guerra mil.csv',
                                    default_guerra_preguntas)

class RoundedButton(Button):
    """
    Clase personalizada para botones con bordes completamente redondeados y aspecto ovalado.
    """
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.background_normal = ' '
        self.background_down = ' '
        self.font_size = kwargs.get('font_size', '20sp')
        self.color = kwargs.get('color', (1, 1, 1, 1))  
        self.size_hint = kwargs.get('size_hint', (1, None))
        self.height = kwargs.get('height', 50)
        self.background_color = kwargs.get('background_color', BUTTON_COLOR)
        with self.canvas.before:
            Color(*self.background_color)
            self.round_rect = RoundedRectangle(pos=self.pos, size=self.size,
                                               radius=[self.height / 2])
        self.bind(pos=self.update_rect, size=self.update_rect,
                  background_color=self.update_color)

    def update_rect(self, *args):
        self.round_rect.pos = self.pos
        self.round_rect.size = self.size
        self.round_rect.radius = [self.height / 2]

    def update_color(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.background_color)
            self.round_rect = RoundedRectangle(pos=self.pos, size=self.size,
                                               radius=[self.height / 2])

class StartScreen(Screen):
    """
    Pantalla de inicio con 3 botones para seleccionar un tema.
    """
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        main_layout = BoxLayout(orientation='vertical')

        self.header_layout = BoxLayout(size_hint=(1, 0.15))
        with self.header_layout.canvas.before:
            Color(0.0, 0.6, 0.9, 1)  
            self.header_rect = Rectangle(pos=self.header_layout.pos,
                                         size=self.header_layout.size)
        self.header_layout.bind(size=self.update_header_footer_rect,
                                pos=self.update_header_footer_rect)

        self.header_label = Label(
            text='[color=#00008B]GEORT[/color] [color=#00CC00]BETA[/color]',
            font_size='40sp',
            bold=True,
            markup=True,  
            halign='center',
            valign='middle',
            size_hint=(1, 1)
        )
        self.header_label.bind(size=self.update_header_label_text_size)
        self.header_layout.add_widget(self.header_label)

        # Centro: Tres botones completamente ovalados y centrados verticalmente
        center_layout = AnchorLayout(anchor_y='center', size_hint=(1, 0.7))

        buttons_layout = BoxLayout(orientation='vertical', spacing=40,
                                   size_hint=(0.9, None))
        buttons_layout.bind(minimum_height=buttons_layout.setter('height'))

        # Botón 1: "Independencia de Colombia"
        btn_independencia = RoundedButton(
            text='Independencia de Colombia',
            background_color=BUTTON_COLOR,  # Verde brillante
            font_size='30sp',
            height=80  # Aumentar altura para una forma más ovalada
        )
        btn_independencia.bind(on_press=lambda x: self.navigate_to_quiz('Independencia de Colombia'))

        # Botón 2: "Batalla de Boyacá"
        btn_batalla = RoundedButton(
            text='Batalla de Boyacá',
            background_color=BUTTON_COLOR,
            font_size='30sp',
            height=80
        )
        btn_batalla.bind(on_press=lambda x: self.navigate_to_quiz('Batalla de Boyacá'))

        # Botón 3: "Guerra de los Mil Días"
        btn_guerra = RoundedButton(
            text='Guerra de los Mil Días',
            background_color=BUTTON_COLOR,
            font_size='30sp',
            height=80
        )
        btn_guerra.bind(on_press=lambda x: self.navigate_to_quiz('Guerra de los Mil Días'))

        # Añadir los botones al layout de botones
        buttons_layout.add_widget(btn_independencia)
        buttons_layout.add_widget(btn_batalla)
        buttons_layout.add_widget(btn_guerra)

        # Añadir el layout de botones al AnchorLayout
        center_layout.add_widget(buttons_layout)

        # Footer
        self.footer_layout = BoxLayout(orientation='horizontal',
                                       size_hint=(1, 0.15))
        with self.footer_layout.canvas.before:
            Color(0.0, 0.7, 0.0, 1)  # Verde claro
            self.footer_rect = Rectangle(pos=self.footer_layout.pos,
                                         size=self.footer_layout.size)
        self.footer_layout.bind(size=self.update_header_footer_rect,
                                pos=self.update_header_footer_rect)

        self.footer_label = Label(
            text='[color=#006400]Desarrollado por: [/color][color=#32CD32]GEORT TEAM[/color]',
            font_size='24sp',
            markup=True,
            halign='center',
            valign='middle',
            size_hint=(1, 1)
        )
        self.footer_label.bind(size=self.update_footer_label_text_size)
        self.footer_layout.add_widget(self.footer_label)

        # Añadir todos los layouts al layout principal
        main_layout.add_widget(self.header_layout)
        main_layout.add_widget(center_layout)
        main_layout.add_widget(self.footer_layout)

        self.add_widget(main_layout)

    def navigate_to_quiz(self, topic):
        """
        Navegar a la pantalla de carga con el tema seleccionado.
        """
        loading_screen = self.manager.get_screen('loading_screen')
        loading_screen.selected_topic = topic
        self.manager.current = 'loading_screen'

    def update_header_footer_rect(self, instance, value):
        if instance == self.header_layout:
            self.header_rect.pos = instance.pos
            self.header_rect.size = instance.size
        elif instance == self.footer_layout:
            self.footer_rect.pos = instance.pos
            self.footer_rect.size = instance.size

    def update_header_label_text_size(self, instance, value):
        self.header_label.text_size = instance.size

    def update_footer_label_text_size(self, instance, value):
        self.footer_label.text_size = instance.size

class LoadingScreen(Screen):
    """
    Pantalla de carga que muestra un mensaje de 'Iniciando...' y una barra de progreso.
    """
    selected_topic = StringProperty('')

    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)
        self.progress_bar = None
        self.progress_value = 0
        self.build_ui()

    def build_ui(self):
        # Layout principal vertical
        main_layout = BoxLayout(orientation='vertical')

        # Header
        self.header_layout = BoxLayout(size_hint=(1, 0.15))
        with self.header_layout.canvas.before:
            Color(0.0, 0.6, 0.9, 1)  # Azul claro
            self.header_rect = Rectangle(pos=self.header_layout.pos,
                                         size=self.header_layout.size)
        self.header_layout.bind(size=self.update_header_footer_rect,
                                pos=self.update_header_footer_rect)

        self.header_label = Label(
            text='[color=#00008B]GEORT[/color] [color=#00CC00]BETA[/color]',
            font_size='40sp',
            bold=True,
            markup=True,  # Habilitar markup para colores
            halign='center',
            valign='middle',
            size_hint=(1, 1)
        )
        self.header_label.bind(size=self.update_header_label_text_size)
        self.header_layout.add_widget(self.header_label)

        # Centro: Contenido de carga
        center_layout = BoxLayout(orientation='vertical',
                                  size_hint=(1, 0.7),
                                  spacing=20,
                                  padding=(50, 0, 50, 0))

        # Espacio vacío para centrar verticalmente
        center_layout.add_widget(Widget(size_hint=(1, 0.3)))

        # Label 'Iniciando...'
        self.loading_label = Label(
            text='Iniciando...',
            font_size='30sp',
            color=(0, 0, 0, 1),  # Texto negro
            size_hint=(1, None),
            height=50,
            halign='center',
            valign='middle'
        )
        self.loading_label.bind(size=self.update_label_text_size)
        center_layout.add_widget(self.loading_label)

        # Barra de progreso personalizada
        self.progress_bar = ProgressBar(max=100, value=0, size_hint=(1, None), height=30)
        with self.progress_bar.canvas.before:
            Color(0.0, 0.8, 0.0, 1)  # Color verde brillante
            self.round_rect = RoundedRectangle(pos=self.progress_bar.pos, size=self.progress_bar.size,
                                               radius=[15])  # Radio para hacerla ovalada
        self.progress_bar.bind(pos=self.update_progress_bar_rect, size=self.update_progress_bar_rect)
        center_layout.add_widget(self.progress_bar)

        # Espacio vacío adicional
        center_layout.add_widget(Widget(size_hint=(1, 0.7)))

        # Footer
        self.footer_layout = BoxLayout(orientation='horizontal',
                                       size_hint=(1, 0.15))
        with self.footer_layout.canvas.before:
            Color(0.0, 0.7, 0.0, 1)  # Verde claro
            self.footer_rect = Rectangle(pos=self.footer_layout.pos,
                                         size=self.footer_layout.size)
        self.footer_layout.bind(size=self.update_header_footer_rect,
                                pos=self.update_header_footer_rect)

        self.footer_label = Label(
            text='[color=#006400]Desarrollado por: [/color][color=#32CD32]GEORT TEAM[/color]',
            font_size='24sp',
            markup=True,
            halign='center',
            valign='middle',
            size_hint=(1, 1)
        )
        self.footer_label.bind(size=self.update_footer_label_text_size)
        self.footer_layout.add_widget(self.footer_label)

        # Añadir todos los layouts al layout principal
        main_layout.add_widget(self.header_layout)
        main_layout.add_widget(center_layout)
        main_layout.add_widget(self.footer_layout)

        self.add_widget(main_layout)

    def update_header_footer_rect(self, instance, value):
        if instance == self.header_layout:
            self.header_rect.pos = instance.pos
            self.header_rect.size = instance.size
        elif instance == self.footer_layout:
            self.footer_rect.pos = instance.pos
            self.footer_rect.size = instance.size

    def update_header_label_text_size(self, instance, value):
        self.header_label.text_size = instance.size

    def update_footer_label_text_size(self, instance, value):
        self.footer_label.text_size = instance.size

    def update_label_text_size(self, instance, value):
        instance.text_size = (instance.width, None)

    def update_progress_bar_rect(self, instance, value):
        self.round_rect.pos = instance.pos
        self.round_rect.size = instance.size

    def on_enter(self):
        # Cuando se muestra la pantalla, iniciar el progreso
        self.progress_value = 0
        self.progress_bar.value = 0
        self.event = Clock.schedule_interval(self.update_progress, 0.05)  # Actualizar cada 0.05 segundos

    def update_progress(self, dt):
        self.progress_value += 1
        self.progress_bar.value = self.progress_value
        if self.progress_value >= 100:
            Clock.unschedule(self.event)
            # Navegar a QuizScreen y pasar el tema seleccionado
            quiz_screen = self.manager.get_screen('quiz_screen')
            quiz_screen.selected_topic = self.selected_topic
            self.manager.current = 'quiz_screen'

    def on_leave(self):
        # Reiniciar el progreso cuando se sale de la pantalla
        self.progress_value = 0
        self.progress_bar.value = 0

class InitialLoadingScreen(Screen):
    """
    Pantalla de carga inicial que muestra un mensaje de 'Cargando...' y una barra de progreso.
    """
    def __init__(self, **kwargs):
        super(InitialLoadingScreen, self).__init__(**kwargs)
        self.progress_bar = None
        self.progress_value = 0
        self.build_ui()

    def build_ui(self):
        # Layout principal vertical
        main_layout = BoxLayout(orientation='vertical')

        # Header
        self.header_layout = BoxLayout(size_hint=(1, 0.15))
        with self.header_layout.canvas.before:
            Color(0.0, 0.6, 0.9, 1)  # Azul claro
            self.header_rect = Rectangle(pos=self.header_layout.pos,
                                         size=self.header_layout.size)
        self.header_layout.bind(size=self.update_header_footer_rect,
                                pos=self.update_header_footer_rect)

        self.header_label = Label(
            text='[color=#00008B]GEORT[/color] [color=#00CC00]BETA[/color]',
            font_size='40sp',
            bold=True,
            markup=True,  # Habilitar markup para colores
            halign='center',
            valign='middle',
            size_hint=(1, 1)
        )
        self.header_label.bind(size=self.update_header_label_text_size)
        self.header_layout.add_widget(self.header_label)

        # Centro: Contenido de carga
        center_layout = BoxLayout(orientation='vertical',
                                  size_hint=(1, 0.7),
                                  spacing=20,
                                  padding=(50, 0, 50, 0))

        # Espacio vacío para centrar verticalmente
        center_layout.add_widget(Widget(size_hint=(1, 0.3)))

        # Label 'Cargando...'
        self.loading_label = Label(
            text='Cargando...',
            font_size='30sp',
            color=(1, 0.5, 0, 1),  # Naranja
            size_hint=(1, None),
            height=50,
            halign='center',
            valign='middle'
        )
        self.loading_label.bind(size=self.update_label_text_size)
        center_layout.add_widget(self.loading_label)

        # Barra de progreso personalizada
        self.progress_bar = ProgressBar(max=100, value=0, size_hint=(1, None), height=30)
        with self.progress_bar.canvas.before:
            Color(0.0, 0.8, 0.0, 1)  # Color verde brillante
            self.round_rect = RoundedRectangle(pos=self.progress_bar.pos, size=self.progress_bar.size,
                                               radius=[15])  # Radio para hacerla ovalada
        self.progress_bar.bind(pos=self.update_progress_bar_rect, size=self.update_progress_bar_rect)
        center_layout.add_widget(self.progress_bar)

        # Espacio vacío adicional
        center_layout.add_widget(Widget(size_hint=(1, 0.7)))

        # Footer
        self.footer_layout = BoxLayout(orientation='horizontal',
                                       size_hint=(1, 0.15))
        with self.footer_layout.canvas.before:
            Color(0.0, 0.7, 0.0, 1)  # Verde claro
            self.footer_rect = Rectangle(pos=self.footer_layout.pos,
                                         size=self.footer_layout.size)
        self.footer_layout.bind(size=self.update_header_footer_rect,
                                pos=self.update_header_footer_rect)

        self.footer_label = Label(
            text='[color=#006400]Desarrollado por: [/color][color=#32CD32]GEORT TEAM[/color]',
            font_size='24sp',
            markup=True,
            halign='center',
            valign='middle',
            size_hint=(1, 1)
        )
        self.footer_label.bind(size=self.update_footer_label_text_size)
        self.footer_layout.add_widget(self.footer_label)

        # Añadir todos los layouts al layout principal
        main_layout.add_widget(self.header_layout)
        main_layout.add_widget(center_layout)
        main_layout.add_widget(self.footer_layout)

        self.add_widget(main_layout)

    def update_header_footer_rect(self, instance, value):
        if instance == self.header_layout:
            self.header_rect.pos = instance.pos
            self.header_rect.size = instance.size
        elif instance == self.footer_layout:
            self.footer_rect.pos = instance.pos
            self.footer_rect.size = instance.size

    def update_header_label_text_size(self, instance, value):
        self.header_label.text_size = instance.size

    def update_footer_label_text_size(self, instance, value):
        self.footer_label.text_size = instance.size

    def update_label_text_size(self, instance, value):
        instance.text_size = (instance.width, None)

    def update_progress_bar_rect(self, instance, value):
        self.round_rect.pos = instance.pos
        self.round_rect.size = instance.size

    def on_enter(self):
        # Cuando se muestra la pantalla, iniciar el progreso
        self.progress_value = 0
        self.progress_bar.value = 0
        self.event = Clock.schedule_interval(self.update_progress, 0.05)  # Actualizar cada 0.05 segundos

    def update_progress(self, dt):
        self.progress_value += 1
        self.progress_bar.value = self.progress_value
        if self.progress_value >= 100:
            Clock.unschedule(self.event)
            # Navegar a StartScreen
            self.manager.current = 'start_screen'

    def on_leave(self):
        # Reiniciar el progreso cuando se sale de la pantalla
        self.progress_value = 0
        self.progress_bar.value = 0

class BarChartWidget(Widget):
    """
    Widget personalizado para mostrar un gráfico de barras.
    """
    def __init__(self, correctas, incorrectas, **kwargs):
        super(BarChartWidget, self).__init__(**kwargs)
        self.correctas = correctas
        self.incorrectas = incorrectas
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.labels = []

    def update_canvas(self, *args):
        self.canvas.clear()
        for label in self.labels:
            self.remove_widget(label)
        self.labels.clear()

        with self.canvas:
            # Colores
            correct_color = (0.0, 0.8, 0.0, 1)  # Verde
            incorrect_color = (0.8, 0.0, 0.0, 1)  # Rojo

            total = self.correctas + self.incorrectas
            if total > 0:
                correct_height_ratio = self.correctas / total
                incorrect_height_ratio = self.incorrectas / total
            else:
                correct_height_ratio = incorrect_height_ratio = 0

            max_height = self.height * 0.6  # Dejar espacio para etiquetas

            # Ancho de las barras
            bar_width = self.width * 0.2

            # Posiciones de las barras
            correct_x = self.x + self.width * 0.25 - bar_width / 2
            incorrect_x = self.x + self.width * 0.75 - bar_width / 2

            # Alturas de las barras
            correct_height = correct_height_ratio * max_height
            incorrect_height = incorrect_height_ratio * max_height

            # Dibujar barra de correctas
            Color(*correct_color)
            Rectangle(pos=(correct_x, self.y), size=(bar_width, correct_height))

            # Dibujar barra de incorrectas
            Color(*incorrect_color)
            Rectangle(pos=(incorrect_x, self.y), size=(bar_width, incorrect_height))

        # Crear etiquetas
        correct_label = Label(
            text=f'Correctas\n{self.correctas}',
            pos=(correct_x, self.y + correct_height + 10),
            size_hint=(None, None),
            size=(bar_width, 50),
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1),
            markup=True
        )
        incorrect_label = Label(
            text=f'Incorrectas\n{self.incorrectas}',
            pos=(incorrect_x, self.y + incorrect_height + 10),
            size_hint=(None, None),
            size=(bar_width, 50),
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1),
            markup=True
        )
        self.add_widget(correct_label)
        self.add_widget(incorrect_label)
        self.labels.extend([correct_label, incorrect_label])

class QuizScreen(Screen):
    """
    Pantalla que muestra el cuestionario generado.
    """
    selected_topic = StringProperty('')

    def __init__(self, **kwargs):
        super(QuizScreen, self).__init__(**kwargs)
        self.current_question_index = 0
        self.score = 0
        self.questions = []
        self.start_time = 0  # Variable para almacenar el tiempo de inicio
        self.build_ui()

    def build_ui(self):
        # Layout principal vertical
        main_layout = BoxLayout(orientation='vertical')

        # Header
        self.header_layout = BoxLayout(size_hint=(1, 0.15))
        with self.header_layout.canvas.before:
            Color(0.0, 0.6, 0.9, 1)  # Azul claro
            self.header_rect = Rectangle(pos=self.header_layout.pos,
                                         size=self.header_layout.size)
        self.header_layout.bind(size=self.update_header_footer_rect,
                                pos=self.update_header_footer_rect)

        self.header_label = Label(
            text='',  # Inicialmente vacío; se actualizará en on_enter
            font_size='40sp',
            bold=True,
            markup=True,
            halign='center',
            valign='middle',
            size_hint=(1, 1)
        )
        self.header_label.bind(size=self.update_header_label_text_size)
        self.header_layout.add_widget(self.header_label)

        # Centro: Quiz
        self.center_layout = BoxLayout(orientation='vertical',
                                       size_hint=(1, 0.7),  # Ajustar size_hint para acomodar el footer
                                       spacing=20,
                                       padding=(50, 0, 50, 0))

        # Contenedor para la pregunta con fondo azul oscuro
        self.question_container = BoxLayout(size_hint=(1, None), height=120)
        with self.question_container.canvas.before:
            Color(0.0, 0.0, 0.5, 1)  # Azul oscuro
            self.question_rect = Rectangle(pos=self.question_container.pos,
                                           size=self.question_container.size)
        self.question_container.bind(pos=self.update_question_rect,
                                     size=self.update_question_rect)

        self.question_label = Label(
            text='',
            font_size='24sp',
            color=(1, 1, 1, 1),  # Texto blanco
            halign='center',
            valign='middle',
            markup=True,
            size_hint=(1, 1),
            text_size=(0, 0)
        )
        self.question_label.bind(size=self.update_question_label_text_size)
        self.question_container.add_widget(self.question_label)
        self.center_layout.add_widget(self.question_container)

        # Opciones de respuestas
        self.options_layout = BoxLayout(orientation='vertical', spacing=10,
                                        size_hint=(1, 1))

        self.option_buttons = []
        for i in range(4):
            btn = RoundedButton(
                text='',
                background_color=BUTTON_COLOR,
                on_press=self.on_option_selected
            )
            self.option_buttons.append(btn)
            self.options_layout.add_widget(btn)

        self.center_layout.add_widget(self.options_layout)

        # Footer
        self.footer_layout = BoxLayout(orientation='horizontal',
                                       size_hint=(1, 0.15))
        with self.footer_layout.canvas.before:
            Color(0.0, 0.7, 0.0, 1)  # Verde claro
            self.footer_rect = Rectangle(pos=self.footer_layout.pos,
                                         size=self.footer_layout.size)
        self.footer_layout.bind(size=self.update_header_footer_rect,
                                pos=self.update_header_footer_rect)

        self.footer_label = Label(
            text='[color=#006400]Desarrollado por: [/color][color=#32CD32]GEORT TEAM[/color]',
            font_size='24sp',
            markup=True,
            halign='center',
            valign='middle',
            size_hint=(1, 1)
        )
        self.footer_label.bind(size=self.update_footer_label_text_size)
        self.footer_layout.add_widget(self.footer_label)

        # Añadir todas las secciones al layout principal
        main_layout.add_widget(self.header_layout)
        main_layout.add_widget(self.center_layout)
        main_layout.add_widget(self.footer_layout)

        self.add_widget(main_layout)

    def update_header_footer_rect(self, instance, value):
        if instance == self.header_layout:
            self.header_rect.pos = instance.pos
            self.header_rect.size = instance.size
        elif instance == self.footer_layout:
            self.footer_rect.pos = instance.pos
            self.footer_rect.size = instance.size

    def update_header_label_text_size(self, instance, value):
        self.header_label.text_size = instance.size

    def update_footer_label_text_size(self, instance, value):
        self.footer_label.text_size = instance.size

    def update_question_rect(self, instance, value):
        self.question_rect.pos = instance.pos
        self.question_rect.size = instance.size

    def update_question_label_text_size(self, instance, value):
        self.question_label.text_size = (instance.width - 20, instance.height - 20)

    def aplicar_estilo_colores(self, texto):
        """
        Aplica el mismo estilo de colores que 'GEORT BETA' al texto proporcionado.
        """
        palabras = texto.split()
        mitad = len(palabras) // 2
        primera_parte = ' '.join(palabras[:mitad])
        segunda_parte = ' '.join(palabras[mitad:])
        texto_con_estilo = f"[color=#00008B]{primera_parte}[/color] [color=#00CC00]{segunda_parte}[/color]"
        return texto_con_estilo

    def on_enter(self):
        # Método llamado al entrar en la pantalla
        # Actualizar el header_label con el tema seleccionado y aplicar el estilo de colores
        self.header_label.text = self.aplicar_estilo_colores(self.selected_topic)

        # Cargar las preguntas y mostrar la primera
        self.load_questions()
        self.display_current_question()

        # Registrar el tiempo de inicio del quiz
        self.start_time = time.time()

    def load_questions(self):
        # Cargar preguntas basadas en el tema seleccionado
        if self.selected_topic == 'Independencia de Colombia':
            self.questions = independencia_preguntas.copy()
        elif self.selected_topic == 'Batalla de Boyacá':
            self.questions = boyaca_preguntas.copy()
        elif self.selected_topic == 'Guerra de los Mil Días':
            self.questions = guerra_preguntas.copy()
        else:
            self.questions = []

        # Asegurarse de tener exactamente 6 preguntas
        if len(self.questions) >= 6:
            self.questions = random.sample(self.questions, 6)
        else:
            print("Advertencia: No hay suficientes preguntas, se usarán todas las disponibles.")
        random.shuffle(self.questions)
        self.current_question_index = 0
        self.score = 0

    def display_current_question(self):
        # Mostrar la pregunta actual
        if self.current_question_index < len(self.questions):
            question_data = self.questions[self.current_question_index]
            self.question_label.text = f"Pregunta {self.current_question_index + 1}:\n{question_data['question']}"

            # Mostrar las opciones
            options = question_data['options'].copy()
            random.shuffle(options)  # Mezclar las opciones
            for i, option in enumerate(options):
                btn = self.option_buttons[i]
                btn.text = f"{chr(65 + i)}. {option}"
                btn.background_color = BUTTON_COLOR
                btn.disabled = False
                btn.font_size = '20sp'  # Restablecer tamaño de fuente
                btn.color = (1, 1, 1, 1)  # Restablecer color de texto a blanco

            # Guardar la respuesta correcta
            correct_option_text = question_data['options'][ord(question_data['correct_answer']) - 65]
            self.correct_option_text = correct_option_text
        else:
            self.show_results()

    def on_option_selected(self, instance):
        # Manejar la selección de una opción
        selected_option_text = instance.text[3:]  # Obtener el texto de la opción sin la letra y punto
        if selected_option_text == self.correct_option_text:
            self.score += 1
            # Cambiar a un verde más brillante
            instance.background_color = (0.5, 1.0, 0.0, 1)  # Verde lima
            instance.font_size = '24sp'  # Aumentar tamaño de fuente
        else:
            instance.background_color = (1.0, 0.0, 0.0, 1)  # Rojo
            # Resaltar la respuesta correcta
            for btn in self.option_buttons:
                if btn.text[3:] == self.correct_option_text:
                    btn.background_color = (0.5, 1.0, 0.0, 1)  # Verde lima
                    btn.font_size = '24sp'  # Aumentar tamaño de fuente
                    break

        # Deshabilitar botones
        for btn in self.option_buttons:
            btn.disabled = True

        # Siguiente pregunta
        self.current_question_index += 1
        Clock.schedule_once(lambda dt: self.display_current_question(), 1.5)

    def show_results(self):
        # Calcular el tiempo total
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)

        # Mostrar resultados
        self.question_label.text = (f"¡Quiz Completado!\n"
                                    f"Tu puntuación: {self.score}/{len(self.questions)}\n"
                                    f"Tiempo tomado: {minutes} min {seconds} seg")
        for btn in self.option_buttons:
            btn.opacity = 0  # Ocultar botones

        # Generar el diagrama de barras utilizando Kivy
        self.create_bar_chart()

        # Botón para continuar al cuestionario de experiencia
        self.next_button = RoundedButton(
            text='Continuar',
            background_color=BUTTON_COLOR,
            font_size='24sp',
            on_press=self.show_experience_survey
        )
        self.center_layout.add_widget(self.next_button)

    def create_bar_chart(self):
        correctas = self.score
        incorrectas = len(self.questions) - self.score
        self.chart_widget = BarChartWidget(correctas=correctas, incorrectas=incorrectas, size_hint=(1, None), height=250)
        self.center_layout.add_widget(self.chart_widget)

    def show_experience_survey(self, instance):
        # Remover el botón 'Continuar' y el gráfico
        if hasattr(self, 'next_button'):
            self.center_layout.remove_widget(self.next_button)
        if hasattr(self, 'chart_widget'):
            self.center_layout.remove_widget(self.chart_widget)

        # Crear el cuestionario de experiencia
        self.question_label.text = "¿Cómo fue tu experiencia?"
        self.option_buttons_experience = []
        options = ['Mala', 'Regular', 'Normal', 'Buena']
        for option in options:
            btn = RoundedButton(
                text=option,
                background_color=BUTTON_COLOR,
                font_size='24sp',
                on_press=self.on_experience_selected
            )
            self.option_buttons_experience.append(btn)
            self.center_layout.add_widget(btn)

    def on_experience_selected(self, instance):
        # Guardar la respuesta del usuario
        user_response = instance.text
        self.save_experience_response(user_response)

        # Limpiar los botones de experiencia
        for btn in self.option_buttons_experience:
            self.center_layout.remove_widget(btn)

        # Regresar al menú principal
        self.go_back_to_menu()

    def save_experience_response(self, response):
         # Guardar la respuesta en un archivo CSV
         filename = 'experiencia_usuarios.csv'
         fieldnames = ['Tema', 'Puntuación', 'Tiempo (segundos)', 'Experiencia']
         elapsed_time = time.time() - self.start_time
         data = {
             'Tema': self.selected_topic,
             'Puntuación': f"{self.score}/{len(self.questions)}",
             'Tiempo (segundos)': round(elapsed_time, 2),
             'Experiencia': response
         }
         try:
            with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
                 writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                 # Escribir el encabezado si el archivo está vacío
                 if csvfile.tell() == 0:
                    writer.writeheader()
                 writer.writerow(data)
            print("Respuesta de experiencia guardada correctamente.")
         except Exception as e:
             print(f"Error al guardar la respuesta de experiencia: {e}")

    def go_back_to_menu(self):
        # Remover widgets adicionales
        self.manager.current = 'start_screen'
        self.current_question_index = 0
        self.score = 0
        self.start_time = 0  # Restablecer el tiempo de inicio
        self.question_label.text = ''
        for btn in self.option_buttons:
            btn.opacity = 1  # Mostrar botones
            btn.disabled = False
            btn.background_color = BUTTON_COLOR
            btn.font_size = '20sp'  # Restablecer tamaño de fuente

    def update_question_rect(self, instance, value):
        self.question_rect.pos = instance.pos
        self.question_rect.size = instance.size

class geortApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(InitialLoadingScreen(name='initial_loading_screen'))  # Añadir la pantalla de carga inicial
        sm.add_widget(StartScreen(name='start_screen'))
        sm.add_widget(LoadingScreen(name='loading_screen'))  # Añadir la pantalla de carga
        sm.add_widget(QuizScreen(name='quiz_screen'))
        sm.current = 'initial_loading_screen'  # Establecer la pantalla inicial
        return sm

try:
    geortApp().run()
except Exception as e:
    print(e)
    pass
   
