import os

file_path = "build_html.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Door Image
content = content.replace("background-image: url('epic_heavy_door_1778106660995.png');", "background-image: url('epic_cross_door_1778107042325.png');")

# 2. Slower door opening
content = content.replace("transition: transform 1.5s cubic-bezier(0.645, 0.045, 0.355, 1);", "transition: transform 3.5s cubic-bezier(0.4, 0, 0.2, 1);")

# 3. Scroll modal style changes
old_scroll_modal = """        .scroll-modal {
            width: 90vw; max-width: 600px;
            background-image: url('mystical_ancient_scroll_1778070821283.png');
            background-size: cover; background-position: center;
            border-radius: 20px; box-shadow: 0 30px 100px rgba(0,0,0,0.9), 0 0 80px rgba(229,192,123,0.3);
            padding: 4rem 3rem; text-align: center;
            position: relative;
            transform: translateY(0);
            clip-path: polygon(0 0, 100% 0, 100% 0, 0 0); /* Rolled up completely */
            transition: clip-path 1.5s cubic-bezier(0.25, 1, 0.5, 1) 1.2s; /* Unrolls after doors open */
        }"""
new_scroll_modal = """        .scroll-modal {
            width: 95vw; max-width: 800px;
            max-height: 90vh; overflow-y: auto;
            background-image: url('mystical_ancient_scroll_1778070821283.png');
            background-size: cover; background-position: center;
            border-radius: 20px; box-shadow: 0 30px 100px rgba(0,0,0,0.9), 0 0 80px rgba(229,192,123,0.3);
            padding: 4rem 3rem; text-align: center;
            position: relative;
            transform: translateY(0);
            clip-path: polygon(0 0, 100% 0, 100% 0, 0 0); /* Rolled up completely */
            transition: clip-path 2.5s cubic-bezier(0.25, 1, 0.5, 1) 0.5s; /* Unrolls while doors open */
        }"""
content = content.replace(old_scroll_modal, new_scroll_modal)

old_p_style = "color: #f2f2f2; font-size: 1.1rem; line-height: 1.6; text-shadow: 0 2px 10px rgba(0,0,0,0.8); margin-bottom: 2rem; background: rgba(0,0,0,0.4); padding: 25px; border-radius: 12px; border: 1px solid rgba(229, 192, 123, 0.1); backdrop-filter: blur(10px);"
new_p_style = "color: #f2f2f2; font-size: 1.1rem; line-height: 1.6; text-shadow: 0 2px 10px rgba(0,0,0,0.8); margin-bottom: 2rem; background: rgba(0,0,0,0.4); padding: 35px; border-radius: 12px; border: 1px solid rgba(229, 192, 123, 0.1); backdrop-filter: blur(10px); text-align: left;"
content = content.replace(old_p_style, new_p_style)

# 4. Text replacement in configs
# Find the config blocks and replace scroll_title and scroll_p.
# We will use string slicing or regex.
import re

pt_scroll_p = '''A Sua Chave Diária de Sabedoria Hoje é:<br><br><b>Dois Gravetos: A Cruz Da Viúva</b><br><br>"Ela respondeu: 'Tão certo como vive o Senhor, teu Deus, não tenho pão algum; tenho apenas um punhado de farinha numa tigela e um pouco de azeite num jarro. Estou apanhando uns gravetos para preparar o alimento para mim e para meu filho; depois disso, vamos morrer.'" (1 Reis 17:12)<br><br>A viúva de Sarepta não havia marcado nenhum encontro. Foi buscar madeira para a última refeição — dois gravetos, um filho com fome e a certeza de que aquilo seria o fim. Sem saber, estava preparando Os Dois Gravetos da Última Refeição.<br><br>O detalhe está numa ação de seis palavras: estava apanhando dois gravetos. Na forma como a lenha era disposta para cozinhar no Oriente Médio antigo, dois gravetos cruzados formavam o arranjo natural para o fogo — uma cruz antes que a cruz existisse. A viúva preparava sua morte em forma de cruz sem saber. Gálatas 3:13 afirma que Cristo se tornou maldição pendurado no madeiro. A provisão chegou a ela no exato momento em que suas mãos tocavam o formato da redenção. O que ela enxergava como postura de desespero era, na linguagem de Deus, postura de adoração.<br><br>Quantas vezes você chegou ao seu último punhado? A última reserva, a última paciência, a última tentativa antes de dizer "vamos morrer." Nesse momento exato — não depois — é quando a presença incomoda aparece e muda a pergunta de "quanto me resta?" para "o que Deus está preparando?"<br><br>Olhe para o que está chamando de fim e pergunte o que Deus está montando ali. Não espere a crise acabar para reconhecer o milagre dentro dela. Nas próximas 24 horas, a chave de sabedoria que você está recebendo hoje é que Deus aparece quando você está segurando Os Dois Gravetos da Última Refeição.<br><br>Quais são seus "dois gravetos" hoje — o que você chama de fim e que Deus pode estar chamando de início?'''

en_scroll_p = '''Your Daily Key of Wisdom Today is:<br><br><b>Two Sticks: The Widow's Cross</b><br><br>"She replied, 'As surely as the Lord your God lives, I don't have any bread—only a handful of flour in a jar and a little olive oil in a jug. I am gathering a few sticks to take home and make a meal for myself and my son, that we may eat it—and die.'" (1 Kings 17:12)<br><br>The widow of Zarephath had not made any appointment. She went to fetch wood for the last meal — two sticks, a hungry son, and the certainty that it would be the end. Without knowing, she was preparing The Two Sticks of the Last Meal.<br><br>The detail lies in a six-word action: she was gathering a few sticks. In the way firewood was arranged for cooking in the ancient Middle East, two crossed sticks formed the natural arrangement for a fire — a cross before the cross existed. The widow was preparing her death in the shape of a cross without knowing. Galatians 3:13 states that Christ became a curse by hanging on a tree. Provision reached her at the exact moment her hands touched the shape of redemption. What she saw as a posture of despair was, in God's language, a posture of worship.<br><br>How many times have you reached your last handful? The last reserve, the last patience, the last attempt before saying "we will die." At that exact moment — not later — is when the uncomfortable presence appears and changes the question from "how much do I have left?" to "what is God preparing?"<br><br>Look at what you are calling the end and ask what God is setting up there. Do not wait for the crisis to end to recognize the miracle within it. In the next 24 hours, the key of wisdom you are receiving today is that God appears when you are holding The Two Sticks of the Last Meal.<br><br>What are your "two sticks" today — what you call the end and what God might be calling the beginning?'''

es_scroll_p = '''Tu Llave Diaria de Sabiduría Hoy es:<br><br><b>Dos Leños: La Cruz De La Viuda</b><br><br>"Ella respondió: 'Vive el Señor tu Dios, que no tengo pan cocido; solamente tengo un puñado de harina en la tinaja y un poco de aceite en una vasija. Ahora recogía un par de leños para entrar y prepararlo para mí y para mi hijo, para que lo comamos y nos muramos.'" (1 Reyes 17:12)<br><br>La viuda de Sarepta no había agendado ninguna cita. Fue a buscar leña para la última comida — dos leños, un hijo con hambre y la certeza de que aquello sería el fin. Sin saberlo, estaba preparando Los Dos Leños de la Última Comida.<br><br>El detalle está en una acción de pocas palabras: estaba recogiendo un par de leños. En la forma en que se disponía la leña para cocinar en el antiguo Medio Oriente, dos palos cruzados formaban el arreglo natural para el fuego — una cruz antes de que la cruz existiera. La viuda preparaba su muerte en forma de cruz sin saberlo. Gálatas 3:13 afirma que Cristo se hizo maldición colgado en un madero. La provisión llegó a ella en el momento exacto en que sus manos tocaban la forma de la redención. Lo que ella veía como una postura de desesperación era, en el lenguaje de Dios, una postura de adoración.<br><br>¿Cuántas veces has llegado a tu último puñado? La última reserva, la última paciencia, el último intento antes de decir "vamos a morir". En ese momento exacto — no después — es cuando la presencia incómoda aparece y cambia la pregunta de "¿cuánto me queda?" a "¿qué está preparando Dios?"<br><br>Mira lo que estás llamando el fin y pregunta qué está montando Dios allí. No esperes a que termine la crisis para reconocer el milagro dentro de ella. En las próximas 24 horas, la llave de sabiduría que estás recibiendo hoy es que Dios aparece cuando estás sosteniendo Los Dos Leños de la Última Comida.<br><br>¿Cuáles son tus "dos leños" hoy — lo que llamas el fin y que Dios podría estar llamando el comienzo?'''

# Replace titles with empty
content = re.sub(r'"scroll_title": ".*?"', '"scroll_title": ""', content)

# Replace paragraphs - we need to make sure we don't break string quoting
content = re.sub(r'"scroll_p": \'.*?\'', '"scroll_p": """' + pt_scroll_p + '"""', content, count=1) # PT
content = re.sub(r'"scroll_p": \'.*?\'', '"scroll_p": """' + en_scroll_p + '"""', content, count=1) # EN
content = re.sub(r'"scroll_p": \'.*?\'', '"scroll_p": """' + es_scroll_p + '"""', content, count=1) # ES

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
