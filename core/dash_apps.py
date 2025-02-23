import dash
import pandas as pd
from django.db.models import Sum
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
from assets.models import Property, Department, Contract, Category
from maintenance.models import Maintenance
from movements.models import Movement

def create_dashboard_app():
    # 1. Crie a aplicação
    app = DjangoDash("dashboard", add_bootstrap_links=True)

    # 2. Defina o layout corretamente
    asset_table = dash_table.DataTable(
        id="asset-table",
        columns=[
            {"name": "Nome do Bem", "id": "property__name"},
            {"name": "Departamento", "id": "department__name"},
            {"name": "Categoria", "id": "category__name"},
            {"name": "RFID Tag", "id": "rfid_tag"},
        ],
        style_cell={"textAlign": "left"},
    )

    maintenance_table = dash_table.DataTable(
        id="maintenance-table",
        columns=[
            {"name": "Nome da Manutenção", "id": "property__name"},
            {"name": "Data de Início", "id": "scheduled_date"},
            {"name": "Data de Entrega", "id": "completion_date"},
            {"name": "Custo", "id": "cost"},
            {"name": "Status", "id": "status"},
        ],
        style_cell={"textAlign": "left"},
    )

    contract_table = dash_table.DataTable(
        id="contract-table",
        columns=[
            {"name": "Nome do Contrato", "id": "property__name"},
            {"name": "Fornecedor", "id": "supplier__name"},
            {"name": "Começo do Contrato", "id": "start_date"},
            {"name": "Fim de Contrato", "id": "end_date"},
            {"name": "Valor", "id": "value"},
        ],
        style_cell={"textAlign": "left"},
    )

    movement_table = dash_table.DataTable(
        id="movement-table",
        columns=[
            {"name": "Nome da Movimentação", "id": "property__name"},
            {"name": "Departamento de Origem", "id": "origin_department__name"},
            {"name": "Departamento de Destino", "id": "destination_department__name"},
            {"name": "Registro", "id": "timestamp"},
        ],
        style_cell={"textAlign": "left"},
    )

    # --------------------- Tabela da aba Valor Total (filtra por Categoria) ---------------------

    total_value_table = dash_table.DataTable(
        id="total-value-table",
        columns=[
            {"name": "Categoria", "id": "category"},
            {"name": "Valor Total", "id": "total_value"},
        ],
        style_cell={"textAlign": "left", "padding": "8px"},
        style_header={"backgroundColor": "#f5f5f5", "fontWeight": "bold"},
    )

    # --------------------- Layout Principal ---------------------
    app.layout = html.Div([
        html.H1("Sistema de Gestão Dashboard", className="text-center mb-4"),

        # -------------------------------------------------
        # 1) Dropdown Global de Departamento (4 abas usam)
        # -------------------------------------------------
        html.Div([
            html.H2("Controle de Departamento", className="mt-3"),
            dcc.Dropdown(
                id="department-dropdown",
                options=[],  # Populado via callback
                value=None,
                placeholder="Selecione um Departamento",
                className="mb-3",
            ),

            # -------------------------------------------------
            # 2) Abas
            # -------------------------------------------------
            dcc.Tabs(
                id="department-tabs",
                children=[
                    # Abas que usam Departamento
                    dcc.Tab(
                        label="Bens",
                        children=[
                            html.H4("Bens por Departamento"),
                            asset_table,
                        ]
                    ),
                    dcc.Tab(
                        label="Manutenções",
                        children=[
                            html.H4("Manutenções por Departamento"),
                            maintenance_table,
                        ]
                    ),
                    dcc.Tab(
                        label="Contratos",
                        children=[
                            html.H4("Contratos por Departamento"),
                            contract_table,
                        ]
                    ),
                    dcc.Tab(
                        label="Movimentações",
                        children=[
                            html.H4("Movimentações por Departamento"),
                            movement_table,
                        ]
                    ),

                    # -------------------------------------------------
                    # 3) Aba de Valor Total (Filtra por Categoria)
                    # -------------------------------------------------
                    dcc.Tab(
                        label="Valor Total (Por Categoria)",
                        children=[
                            html.H4("Valor Total por Categoria"),
                            html.Div([
                                dcc.Dropdown(
                                    id="category-dropdown",
                                    options=[],  # Populado via callback
                                    value="all",  # Valor inicial = "all"
                                    placeholder="Selecione uma Categoria",
                                    className="mb-3",
                                ),
                            ]),

                            total_value_table,
                        ]
                    ),
                ]
            ),
        ], className="col-md-12"),
    ])

    # --------------------- Callbacks das 4 primeiras abas (Departamento) ---------------------

    @app.callback(
        [Output("department-dropdown", "options"),
         Output("department-dropdown", "value")],
        [Input("department-dropdown", "value")]
    )
    def update_department_options(selected_value):
        departments = Department.objects.all()
        options = [{"label": dept.name, "value": dept.id} for dept in departments]
        # Se nenhum valor estiver selecionado e houver opções, seleciona o primeiro
        if not selected_value and options:
            selected_value = options[0]["value"]
        return options, selected_value

    @app.callback(
        Output("asset-table", "data"),
        [Input("department-dropdown", "value")]
    )
    def update_asset_table(selected_department):
        if selected_department:
            assets = Property.objects.filter(department_id=selected_department).values(
                "name", "department__name", "category__name", "rfid_tag"
            )
            df = pd.DataFrame(assets)
            if not df.empty:
                df.rename(columns={"name": "property__name"}, inplace=True)
            return df.to_dict("records")
        return []

    @app.callback(
        Output("maintenance-table", "data"),
        [Input("department-dropdown", "value")]
    )
    def update_maintenance_table(selected_department):
        if selected_department:
            maintenances = Maintenance.objects.filter(
                property__department_id=selected_department
            ).values("property__name", "scheduled_date", "completion_date", "cost", "status")
            return pd.DataFrame(maintenances).to_dict("records")
        return []

    @app.callback(
        Output("contract-table", "data"),
        [Input("department-dropdown", "value")]
    )
    def update_contract_table(selected_department):
        if selected_department:
            contracts = Contract.objects.filter(
                property__department_id=selected_department
            ).values("property__name", "supplier__name", "start_date", "end_date", "value")
            return pd.DataFrame(contracts).to_dict("records")
        return []

    @app.callback(
        Output("movement-table", "data"),
        [Input("department-dropdown", "value")]
    )
    def update_movement_table(selected_department):
        if selected_department:
            movements = Movement.objects.filter(
                origin_department_id=selected_department
            ).values("property__name", "origin_department__name", "destination_department__name", "timestamp")
            return pd.DataFrame(movements).to_dict("records")
        return []

    # --------------------- Callback da aba Valor Total (Categoria) ---------------------

    @app.callback(
        # Popula o dropdown de categoria e define valor inicial "all"
        Output("category-dropdown", "options"),
        [Input("category-dropdown", "value")]
    )
    def populate_category_dropdown(_):
        """Carrega todas as categorias + a opção 'all'."""
        categories = Category.objects.all()
        options = [{"label": "Todas as Categorias", "value": "all"}]
        for cat in categories:
            options.append({"label": cat.name, "value": cat.id})
        return options

    @app.callback(
        Output("total-value-table", "data"),
        [Input("category-dropdown", "value")]
    )
    def update_total_value_table(selected_category):
        """
        Se 'all', lista cada categoria e seu total.
        Se for um ID específico, mostra apenas uma linha com o total daquela categoria.
        """
        qs = Property.objects.all()

        if not selected_category:
            # Nenhuma categoria selecionada => retorna vazio
            return []

        if selected_category == "all":
            # Agrupa por categoria e mostra a soma
            data = (
                qs.values("category__name")
                .annotate(total_value=Sum("value"))
                .order_by("category__name")
            )
            # Exemplo de retorno: [{"category": "Móveis", "total_value": 1000}, ...]
            return [
                {
                    "category": item["category__name"] or "Sem Categoria",
                    "total_value": item["total_value"] or 0
                }
                for item in data
            ]
        else:
            # Filtra por uma categoria específica
            data = qs.filter(category_id=selected_category).aggregate(soma=Sum("value"))
            total = data["soma"] or 0

            # Pega o nome da categoria para exibir
            cat = Category.objects.filter(id=selected_category).first()
            cat_name = cat.name if cat else "Desconhecida"

            return [{
                "category": cat_name,
                "total_value": total
            }]

    return app