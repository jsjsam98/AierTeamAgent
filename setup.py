from injector import Injector, Module, provider, singleton
from app_signal import SignalManager
from db import DataStorage


class AppModule(Module):
    @singleton
    @provider
    def provide_signal_manager(self) -> SignalManager:
        return SignalManager()

    @singleton
    @provider
    def provide_data_storage(self) -> DataStorage:
        return DataStorage()

    # @singleton
    # @provider
    # def provide_main_session(self) -> MainSession:
    #     return MainSession(signal_manager=self.provide_signal_manager())

    # @singleton
    # @provider
    # def provide_screen_overlay(self) -> ScreenOverlay:
    #     return ScreenOverlay(signal_manager=self.provide_signal_manager())


injector = Injector([AppModule()])
