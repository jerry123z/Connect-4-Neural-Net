from abc import ABC, abstractmethod


class AbstractGameState(ABC):

    @abstractmethod
    def game_result(self):
        """
        this property should return:
            positive value if player #1 wins
            negative value if player #2 wins
            0 if there is a draw
            None if result is unknown
        Returns
        -------
        int
        """
        pass

    @abstractmethod
    def is_game_over(self):
        """
        boolean indicating if the game is over
        Returns
        boolean
        """
        pass

    @abstractmethod
    def play(self, action):
        """
        consumes action and returns resulting TwoPlayersAbstractGameState
        Returns
        AbstractGameState
        """
        pass

    @abstractmethod
    def get_legal_actions(self):
        """
        returns list of legal action at current game state
        Returns
        -------
        list of AbstractGameAction
        """
        pass
