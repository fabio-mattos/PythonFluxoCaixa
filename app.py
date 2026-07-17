"""Interface gráfica para atualização do saldo FAPEU na planilha de fluxo de caixa."""
from __future__ import annotations

import queue
import threading
from pathlib import Path

import customtkinter as ctk
from tkinter import messagebox

from config import load_db_config
from database import buscar_saldo_fapeu
from excel_writer import atualizar_planilha

BASE_DIR = Path(__file__).resolve().parent
PLANILHA_PATH = BASE_DIR / "FLUXO DE CAIXA_labtrans_13_07.xlsx"

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Fluxo de Caixa FAPEU")
        self.geometry("440x280")
        self.resizable(False, False)

        self._resultado: queue.Queue = queue.Queue()
        self._executando = False

        self._montar_layout()

    def _montar_layout(self) -> None:
        container = ctk.CTkFrame(self, corner_radius=16)
        container.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(
            container,
            text="Fluxo de Caixa FAPEU",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(pady=(24, 8))

        self.status_label = ctk.CTkLabel(
            container, text="Pronto para atualizar", text_color="gray"
        )
        self.status_label.pack(pady=(0, 12))

        self.progress_bar = ctk.CTkProgressBar(
            container, mode="indeterminate", corner_radius=8
        )

        self.btn_atualizar = ctk.CTkButton(
            container,
            text="Atualizar Planilha",
            corner_radius=20,
            height=44,
            command=self._on_atualizar_click,
        )
        self.btn_atualizar.pack(fill="x", padx=30, pady=(4, 12))

        self.btn_sair = ctk.CTkButton(
            container,
            text="Sair",
            corner_radius=20,
            height=44,
            fg_color="#B3261E",
            hover_color="#8C1D18",
            command=self._on_sair_click,
        )
        self.btn_sair.pack(fill="x", padx=30, pady=(0, 24))

    def _on_sair_click(self) -> None:
        if self._executando and not messagebox.askyesno(
            "Sair", "A atualização está em andamento. Deseja realmente sair?"
        ):
            return
        self.destroy()

    def _on_atualizar_click(self) -> None:
        if self._executando:
            return
        self._executando = True
        self.btn_atualizar.configure(state="disabled")
        self.btn_sair.configure(state="disabled")
        self.status_label.configure(text="Atualizando planilha...", text_color="gray")
        self.progress_bar.pack(fill="x", padx=30, pady=(0, 16))
        self.progress_bar.start()

        threading.Thread(target=self._executar_atualizacao, daemon=True).start()
        self.after(100, self._checar_resultado)

    def _executar_atualizacao(self) -> None:
        try:
            config = load_db_config()
            linhas = buscar_saldo_fapeu(config)
            atualizar_planilha(PLANILHA_PATH, linhas)
            self._resultado.put(("sucesso", len(linhas)))
        except Exception as exc:  # captura para exibir na UI, não deixar a thread matar o app
            self._resultado.put(("erro", str(exc)))

    def _checar_resultado(self) -> None:
        try:
            status, dado = self._resultado.get_nowait()
        except queue.Empty:
            self.after(100, self._checar_resultado)
            return

        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.btn_atualizar.configure(state="normal")
        self.btn_sair.configure(state="normal")
        self._executando = False

        if status == "sucesso":
            self.status_label.configure(
                text=f"Planilha atualizada ({dado} projeto(s))", text_color="#2E7D32"
            )
            messagebox.showinfo(
                "Concluído",
                f"Planilha atualizada com sucesso!\n{dado} projeto(s) gravado(s) na aba saldoFAPEU.",
            )
        else:
            self.status_label.configure(text="Falha na atualização", text_color="#B3261E")
            messagebox.showerror("Erro ao atualizar", dado)


def main() -> None:
    App().mainloop()


if __name__ == "__main__":
    main()
