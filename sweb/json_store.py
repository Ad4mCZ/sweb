import copy
import json
import logging
import os
from typing import Any

from .utils import show_critical_error

log = logging.getLogger(__name__)


class JsonStore:
    """Spolecny zaklad pro data ulozena v JSON souboru (nastaveni, zalozky, adblock...).

    - pri prvnim spusteni vytvori soubor s vychozimi hodnotami
    - doplni chybejici klice z vychozich hodnot (napr. po aktualizaci aplikace)
    - pri chybe bud zobrazi kritickou chybu a ukonci aplikaci (critical=True),
      nebo jen zaloguje chybu a pouzije vychozi hodnoty (critical=False)
    """

    ERROR_TITLE = "Kritická chyba konfigurace"

    def __init__(
        self,
        file_path: str,
        defaults: dict[str, Any],
        file_label: str,
        critical: bool = True,
    ) -> None:
        """
        :param file_path: absolutni cesta k JSON souboru
        :param defaults: slovnik s vychozimi hodnotami
        :param file_label: popis souboru do chybove hlasky v 2. padu,
                           napr. "konfiguračního souboru" nebo "souboru se záložkami"
        :param critical: pokud True, chyba cteni/zapisu ukonci aplikaci
        """
        self.file_path = file_path
        self.defaults = defaults
        self.file_label = file_label
        self.critical = critical

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        log.info("Loading %s from: %s", os.path.basename(file_path), file_path)

        self.data: dict[str, Any] = self.load()

    def _default_copy(self) -> dict[str, Any]:
        # deepcopy, aby se vnorene seznamy/slovniky nesdilely s self.defaults
        return copy.deepcopy(self.defaults)

    def _handle_error(self, action: str, error: Exception) -> None:
        log.error("Error while %s %s: %s", action, self.file_path, error)
        if self.critical:
            verb = "čtení" if action == "reading" else "ukládání"
            # show_critical_error ukonci aplikaci
            show_critical_error(
                title=self.ERROR_TITLE,
                message=f"Chyba při {verb} {self.file_label}!\n\nAplikaci nelze bezpečně spustit a bude ukončena.",
                error_detail=str(error),
            )

    def load(self) -> dict[str, Any]:
        if not os.path.exists(self.file_path):
            data = self._default_copy()
            self.save(data)
            return data

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("Kořenový prvek JSON souboru musí být objekt (slovník).")
        except Exception as e:
            self._handle_error("reading", e)
            return self._default_copy()

        # doplneni chybejicich klicu
        missing = {k: v for k, v in self.defaults.items() if k not in data}
        if missing:
            data.update(copy.deepcopy(missing))
            self.save(data)

        return data

    def save(self, data: dict[str, Any] | None = None) -> None:
        if data is None:
            data = self.data
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self._handle_error("saving", e)

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.data.get(key, self.defaults.get(key, fallback))

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        self.save()
