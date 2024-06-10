from nicegui import ui, app
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
BOARD_DIR = PROJECT_ROOT / "data" / "board"

graph_temp = """
    graph LR
    subgraph \u5e7c\u5e74\u671f
    botamon(<img src='/board/output.svg' width='69' height='59.4' /><br>初期局面)
    koromon(<img src='https://digimon.net/cimages/digimon/koromon.jpg' width='40' height='40' /><br>\u30b3\u30ed\u30e2\u30f3)
    end
    subgraph \u6210\u9577\u671f
    agumon(<img src='https://digimon.net/cimages/digimon/agumon.jpg' width='40' height='40' /><br>\u30a2\u30b0\u30e2\u30f3)
    betamon(<img src='https://digimon.net/cimages/digimon/betamon.jpg' width='40' height='40' /><br>\u30d9\u30bf\u30e2\u30f3)
    end
    subgraph \u6210\u719f\u671f
    greymon-first(<img src='https://digimon.net/cimages/digimon/greymon-first.jpg' width='40' height='40' /><br>\u30b0\u30ec\u30a4\u30e2\u30f3)
    tyranomon(<img src='https://digimon.net/cimages/digimon/tyranomon.jpg' width='40' height='40' /><br>\u30c6\u30a3\u30e9\u30ce\u30e2\u30f3)
    devimon(<img src='https://digimon.net/cimages/digimon/devimon.jpg' width='40' height='40' /><br>\u30c7\u30d3\u30e2\u30f3)
    meramon(<img src='https://digimon.net/cimages/digimon/meramon.jpg' width='40' height='40' /><br>\u30e1\u30e9\u30e2\u30f3)
    airdramon(<img src='https://digimon.net/cimages/digimon/airdramon.jpg' width='40' height='40' /><br>\u30a8\u30a2\u30c9\u30e9\u30e2\u30f3)
    seadramon(<img src='https://digimon.net/cimages/digimon/seadramon.jpg' width='40' height='40' /><br>\u30a8\u30a2\u30c9\u30e9\u30e2\u30f3)
    numemon(<img src='https://digimon.net/cimages/digimon/numemon.jpg' width='40' height='40' /><br>\u30cc\u30e1\u30e2\u30f3)
    end
    subgraph \u5b8c\u5168\u4f53
    metalgreymon-v(<img src='https://digimon.net/cimages/digimon/metalgreymon-v.jpg' width='40' height='40' /><br>\u30e1\u30bf\u30eb\u30b0\u30ec\u30a4\u30e2\u30f3)
    mamemon(<img src='https://digimon.net/cimages/digimon/mamemon.jpg' width='40' height='40' /><br>\u30de\u30e1\u30e2\u30f3)
    monzaemon(<img src='https://digimon.net/cimages/digimon/monzaemon.jpg' width='40' height='40' /><br>\u3082\u3093\u3056\u3048\u30e2\u30f3)
    end
    botamon-->koromon
    koromon-->agumon
    koromon-->betamon
    agumon-->greymon-first
    agumon-->tyranomon
    agumon-->devimon
    betamon-->devimon
    agumon-->meramon
    betamon-->meramon
    betamon-->airdramon
    betamon-->seadramon
    agumon-->numemon
    betamon-->numemon
    greymon-first-->metalgreymon-v
    devimon-->metalgreymon-v
    airdramon-->metalgreymon-v
    tyranomon-->mamemon
    meramon-->mamemon
    seadramon-->mamemon
    numemon-->monzaemon"""

html = """<body>
  <div id="app"></div>
</body>"""


def draw_graph(graph: str = graph_temp):
    head = (
        """
<head>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/mermaid/6.0.0/mermaid.css" rel="stylesheet" />
  <script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/6.0.0/mermaid.js"></script>
  <script>
    window.onload = function () {
      var mermaidAPI = mermaid.mermaidAPI;
      var config = {
        htmlLabels: true,
        flowchart: {
          useMaxWidth: true,
        },
      };
      mermaid.initialize(config);
      var element = document.getElementById("app");
      var insertSvg = function (svgCode, bindFunctions) {
        element.innerHTML = svgCode;
      };
"""
        f"""
      var graphDefinition = `{graph}
      `;
"""
        """
      var graph = mermaidAPI.render("mermaid", graphDefinition, insertSvg);
    };
  </script>
</head>
"""
    )
    print(head)
    app.add_static_files("/board", BOARD_DIR)
    ui.add_head_html(head)
    ui.html(html)
