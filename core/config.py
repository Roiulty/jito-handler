import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Solana
    SOL_MAINNET = "https://api.mainnet-beta.solana.com"
    SOL_DEVNET = "https://api.devnet.solana.com"
    SOL_TESTNET = "https://api.testnet.solana.com"

    # Jito
    JITO_MAINNET = "https://mainnet.block-engine.jito.wtf"
    JITO_TESTNET = "https://dallas.testnet.block-engine.jito.wtf"
    BUNDLE_ENDPOINT = "/api/v1/bundles"
    TRANSACTION_ENDPOINT = "/api/v1/transactions"

    MAIN_BACKUP_TIP_ACCOUNTS = [
        "96gYZGLnJYVFmbjzopPSU6QiEV5fGqZNyN9nmNhvrZU5",
        "HFqU5x63VTqvQss8hp11i4wVV8bD44PvwucfZ2bU7gRe",
        "Cw8CFyM9FkoMi7K7Crf6HNQqf4uEMzpKw6QNghXLvLkY",
        "ADaUMid9yfUytqMBgopwjb2DTLSokTSzL1zt6iGPaS49",
        "DfXygSm4jCyNCybVYYK6DwvWqjKee8pbDmJGcLWNDXjh",
        "ADuUkR4vqLUMWXxW9gh6D6L8pMSawimctcNZ5pGwDcEt",
        "DttWaMuVvTiduZRnguLF7jNxTgiMBZ1hyAumKUiL2KRL",
        "3AVi9Tg9Uo68tJfuvoKvqKNWKkC5wPdSSdeBnizKZ6jT"
    ]
    TEST_BACKUP_TIP_ACCOUNTS = [
        "B1mrQSpdeMU9gCvkJ6VsXVVoYjRGkNA7TtjMyqxrhecH",
        "aTtUk2DHgLhKZRDjePq6eiHRKC1XXFMBiSUfQ2JNDbN",
        "E2eSqe33tuhAHKTrwky5uEjaVqnb2T9ns6nHHUrN8588",
        "4xgEmT58RwTNsF5xm2RMYCnR1EVukdK8a1i2qFjnJFu3",
        "EoW3SUQap7ZeynXQ2QJ847aerhxbPVr843uMeTfc9dxM",
        "ARTtviJkLLt6cHGQDydfo1Wyk6M4VGZdKZ2ZhdnJL336",
        "9n3d1K5YD2vECAbRFhFFGYNNjiXtHXJWn9F31t89vsAV",
        "9ttgPBBhRYFuQccdR1DSnb7hydsWANoDsV3P9kaGMCEh",
    ]

    # Project
    SOLANA_PUBLIC_KEY = os.getenv('SOLANA_PUBLIC_KEY')
    ENVIRONMENT = "DEV"
