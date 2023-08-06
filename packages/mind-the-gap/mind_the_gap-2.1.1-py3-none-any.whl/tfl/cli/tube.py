from typing import List, Optional

import typer
from dateparser import parse
from rich import box
from rich.console import Console
from rich.style import Style
from rich.table import Table
from rich.theme import Theme

from tfl.api.line import by_id, by_mode
from tfl.api.presentation.entities.line import LineStatus

table = Table(box=box.SIMPLE, padding=0)

table.add_column("Line", justify="right", style="cyan", no_wrap=True)
table.add_column("Status", style="magenta")


padding = 18

app = typer.Typer()

BASE_STYLE = Style(bold=True, color="white", italic=True)
line_styles = {
    "london-overground": Style(bgcolor="#EE7C0E"),
    "dlr": Style(bgcolor="#00A4A7"),
    "central": Style(bgcolor="#E32017"),
    "bakerloo": Style(bgcolor="#B36305"),
    "district": Style(bgcolor="#00782A"),
    "metropolitan": Style(bgcolor="#9B0056"),
    "hammersmith-city": Style(bgcolor="#F3A9BB", color="black"),
    "northern": Style(bgcolor="#000000"),
    "piccadilly": Style(bgcolor="#003688"),
    "victoria": Style(bgcolor="#0098D4"),
    "circle": Style(bgcolor="#FFD300", color="black"),
    "jubilee": Style(bgcolor="#A0A5A9", color="black"),
    "waterloo-city": Style(bgcolor="#95CDBA", color="black"),
}
line_styles = {k: BASE_STYLE + v for k, v in line_styles.items()}

status_severity_style = {"good_service": Style(color="green")}


def summarise_statuses(statuses: List[LineStatus]) -> str:

    agg = []
    for status in statuses:
        for validity_period in status.validityPeriods:
            from_date = parse(validity_period.fromDate)
            to_date = parse(validity_period.toDate)
            is_now = validity_period.isNow
            agg.append(
                from_date.strftime("%m/%d/%Y, %H:%M:%S")
                + " "
                + to_date.strftime("%m/%d/%Y, %H:%M:%S")
                + " "
                + str(is_now)
            )
    #     if status.statusSeverity == 10:
    #         agg.append("[good_service]Good service[/good_service]")

    return " ".join(agg)


console = Console(theme=Theme({**line_styles, **status_severity_style}))


@app.command()
def status(line: Optional[str] = typer.Argument(None)) -> None:
    if line is None:
        show_all_statuses()
    else:
        line_data = by_id(line, status=True, detail=True)[0]
        console.print(f" [{line_data.id}]{line_data.name}[/{line_data.id}] ")
        for status in line_data.lineStatuses:
            console.print(status.disruption.description)


def show_all_statuses():
    lines = []
    for mode in ["dlr", "overground", "tube"]:
        lines.extend(by_mode(mode, status=True))
    for line in lines:
        table.add_row(f" [{line.id}]{line.id:>18} [/{line.id}]", summarise_statuses(line.lineStatuses))
    console.print(table)
