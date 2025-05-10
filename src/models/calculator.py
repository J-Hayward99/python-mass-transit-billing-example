import pandas as pd
from pydantic import BaseModel
from models import validators


class TransportCalculator:
    df_zone_prices: pd.DataFrame
    df_station_zones: pd.DataFrame
    df_cap_prices: pd.DataFrame
    df_fee_prices: pd.DataFrame

    df_journey_data: pd.DataFrame

    def __init__(
        self,
        path_zone_prices: str,
        path_station_zones: str,
        path_cap_prices: str,
        path_fee_prices: str,
        path_journey_data: str,
    ):
        self.df_zone_prices = self._load_df(
            path_zone_prices,
            validators.ZonePrice,
        )
        self.df_station_zones = self._load_df(
            path_station_zones,
            validators.StationZones,
        )
        self.df_cap_prices = self._load_df(
            path_cap_prices,
            validators.TravelCap,
        )
        self.df_fee_prices = self._load_df(
            path_fee_prices,
            validators.TravelFee,
        )
        self.df_fee_prices = self._load_df(
            path_journey_data,
            validators.JourneyData,
        )

    def _load_df(
        self, path_file: str, validator: type[BaseModel]
    ) -> pd.DataFrame:
        # Load DataFrmae
        df_raw_csv = pd.read_csv(path_file)
        processed_rows = []

        # Validate and Parse DataFrame
        # NOTE: This handles type conversion and processing like removing £
        for index, row in df_raw_csv.iterrows():
            try:
                record = validator.model_validate(row.to_dict())
                processed_rows.append(record.model_dump())
            except Exception as e:
                raise ValueError(
                    f"Row {index} in '{path_file}' failed validation: {e}"
                )

        # Compile Validated Rows
        return pd.DataFrame(processed_rows)
