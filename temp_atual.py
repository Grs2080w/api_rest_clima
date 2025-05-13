import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor


def process_weather_data(data):
    """Processa os dados meteorológicos com tratamento robusto"""
    processed = []

    for day in data:
        if isinstance(day, list):
            processed.extend(day)
        else:
            processed.append(day)

    df = pd.DataFrame(processed)

    # Verificação de colunas essenciais
    required_cols = [
        "temp_max",
        "temp_min",
        "umi_max",
        "umi_min",
        "hour",
        "dir_air",
        "int_air",
        "sunrise",
        "sunset",
    ]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Colunas faltando: {missing_cols}")

    # Feature engineering aprimorado
    df["temp_diff"] = df["temp_max"] - df["temp_min"]
    df["umi_diff"] = df["umi_max"] - df["umi_min"]

    # Mapeamento de hora para valor numérico (0-23)
    hour_map = {"manha": 8, "tarde": 14, "noite": 20}  # Valores mais representativos
    df["hour_numeric"] = df["hour"].map(hour_map)

    # Processamento da direção do vento
    wind_dir_map = {
        "S-SE": 157.5,
        "SE-S": 135,
        "SE-E": 112.5,
        "E-NE": 67.5,
        "N-NE": 22.5,
        "NE-N": 45,
        "N-NW": 337.5,
        "NW-N": 315,
        "W-NW": 292.5,
        "W-SW": 247.5,
        "SW-S": 225,
        "S-SW": 202.5,
    }
    df["wind_dir_angle"] = df["dir_air"].map(wind_dir_map).fillna(180)
    df["wind_dir_sin"] = np.sin(df["wind_dir_angle"] * np.pi / 180)
    df["wind_dir_cos"] = np.cos(df["wind_dir_angle"] * np.pi / 180)

    # Intensidade do vento
    wind_int_map = {"Fracos": 0, "Moderados": 1, "Fortes": 2}
    df["wind_intensity"] = df["int_air"].map(wind_int_map).fillna(0)

    # Processamento do nascer/por do sol (com regex robusto)
    df["sunrise_hour"] = (
        df["sunrise"].str.extract(r"(\d{1,2})h", expand=False).astype(float)
    )
    df["sunset_hour"] = (
        df["sunset"].str.extract(r"(\d{1,2})h", expand=False).astype(float)
    )
    df["day_length"] = df["sunset_hour"] - df["sunrise_hour"]

    # Cálculo da hora solar normalizada (0 a 1)
    df["solar_progress"] = (df["hour_numeric"] - df["sunrise_hour"]) / (
        df["day_length"] + 1e-6
    )
    df["solar_progress"] = df["solar_progress"].clip(0, 1)

    return df


def simulate_realistic_temp(row):
    """Simula temperatura atual de forma realista entre min e max"""
    # Baseado no progresso solar com variação senoidal
    solar_factor = np.sin(row["solar_progress"] * np.pi)

    # Temperatura base varia entre min e max
    temp = row["temp_min"] + solar_factor * (row["temp_max"] - row["temp_min"])

    # Ajustes secundários (limitados para não ultrapassar min/max)
    umi_effect = -0.5 * (row["umi_max"] - 50) / 50  # Efeito da umidade
    wind_effect = -0.5 * row["wind_intensity"]  # Efeito do vento

    # Aplica os efeitos mantendo dentro dos limites
    temp = np.clip(temp + umi_effect + wind_effect, row["temp_min"], row["temp_max"])

    return round(temp, 1)


weather_data = [
    [
        {
            "day_week": "Sexta-Feira",
            "dir_air": "S-SE",
            "hour": "manha",
            "int_air": "Fracos",
            "sunrise": "06h38",
            "sunset": "18h32",
            "temp_max": 32,
            "temp_max_goes_to": "Em declínio",
            "temp_min": 19,
            "temp_min_goes_to": "Ligeiro Declínio",
            "umi_max": 100,
            "umi_min": 50,
        },
        {
            "day_week": "Sexta-Feira",
            "dir_air": "SE-S",
            "hour": "tarde",
            "int_air": "Fracos",
            "sunrise": "06h38",
            "sunset": "18h32",
            "temp_max": 32,
            "temp_max_goes_to": "Em declínio",
            "temp_min": 19,
            "temp_min_goes_to": "Ligeiro Declínio",
            "umi_max": 100,
            "umi_min": 50,
        },
        {
            "day_week": "Sexta-Feira",
            "dir_air": "S-SE",
            "hour": "noite",
            "int_air": "Fracos",
            "sunrise": "06h38",
            "sunset": "18h32",
            "temp_max": 32,
            "temp_max_goes_to": "Em declínio",
            "temp_min": 19,
            "temp_min_goes_to": "Ligeiro Declínio",
            "umi_max": 100,
            "umi_min": 50,
        },
    ],
    [
        {
            "day_week": "Sábado",
            "dir_air": "SE-S",
            "hour": "manha",
            "int_air": "Fracos",
            "sunrise": "06h38",
            "sunset": "18h31",
            "temp_max": 31,
            "temp_max_goes_to": "Em declínio",
            "temp_min": 20,
            "temp_min_goes_to": "Em declínio",
            "umi_max": 100,
            "umi_min": 50,
        },
        {
            "day_week": "Sábado",
            "dir_air": "SE-E",
            "hour": "tarde",
            "int_air": "Fracos",
            "sunrise": "06h38",
            "sunset": "18h31",
            "temp_max": 31,
            "temp_max_goes_to": "Em declínio",
            "temp_min": 20,
            "temp_min_goes_to": "Em declínio",
            "umi_max": 100,
            "umi_min": 50,
        },
        {
            "day_week": "Sábado",
            "dir_air": "SE-E",
            "hour": "noite",
            "int_air": "Moderados",
            "sunrise": "06h38",
            "sunset": "18h31",
            "temp_max": 31,
            "temp_max_goes_to": "Em declínio",
            "temp_min": 20,
            "temp_min_goes_to": "Em declínio",
            "umi_max": 95,
            "umi_min": 75,
        },
    ],
    {
        "day_week": "Domingo",
        "dir_air": "SE-E",
        "hour": "noite",
        "int_air": "Fracos",
        "sunrise": "06h39",
        "sunset": "18h30",
        "temp_max": 32,
        "temp_max_goes_to": "Ligeiro Declínio",
        "temp_min": 18,
        "temp_min_goes_to": "Em declínio",
        "umi_max": 90,
        "umi_min": 40,
    },
    {
        "day_week": "Segunda-Feira",
        "dir_air": "SE-E",
        "hour": "noite",
        "int_air": "Fracos",
        "sunrise": "06h39",
        "sunset": "18h29",
        "temp_max": 33,
        "temp_max_goes_to": "Em elevação",
        "temp_min": 19,
        "temp_min_goes_to": "Estável",
        "umi_max": 90,
        "umi_min": 30,
    },
    {
        "day_week": "Terça-Feira",
        "dir_air": "E-NE",
        "hour": "noite",
        "int_air": "Fracos",
        "sunrise": "06h39",
        "sunset": "18h28",
        "temp_max": 35,
        "temp_max_goes_to": "Estável",
        "temp_min": 18,
        "temp_min_goes_to": "Estável",
        "umi_max": 90,
        "umi_min": 30,
    },
]

try:
    # Processamento dos dados
    df = process_weather_data(weather_data)

    # Simulação mais realista da temperatura atual
    df["temp_atual"] = df.apply(simulate_realistic_temp, axis=1)

    # Features selecionadas
    features = [
        "temp_min",
        "temp_max",
        "temp_diff",
        "umi_min",
        "umi_max",
        "umi_diff",
        "hour_numeric",
        "wind_intensity",
        "wind_dir_sin",
        "wind_dir_cos",
        "solar_progress",
        "day_length",
    ]

    X = df[features]
    y = df["temp_atual"]

    # Separação dos dados (primeiro dia para teste)
    test_mask = df["day_week"] == df["day_week"].iloc[0]  # Primeiro dia disponível
    X_train, X_test = X[~test_mask], X[test_mask]
    y_train, y_test = y[~test_mask], y[test_mask]

    # Modelo Gradient Boosting com parâmetros otimizados
    model = GradientBoostingRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=4,
        min_samples_leaf=3,
        random_state=42,
    )
    model.fit(X_train, y_train)

    # Previsão com garantia de limites físicos
    df.loc[test_mask, "temp_predicted"] = model.predict(X_test)
    df["temp_predicted"] = np.clip(
        df["temp_predicted"], df["temp_min"], df["temp_max"]
    ).round(1)

    # Resultados para o primeiro dia
    print("\nResultados para o primeiro dia:")
    print(
        df.loc[
            test_mask,
            [
                "day_week",
                "hour",
                "temp_min",
                "temp_max",
                "temp_atual",
                "temp_predicted",
            ],
        ]
    )


except Exception as e:
    print(f"Erro: {str(e)}")
    print("Verifique a estrutura dos seus dados.")
