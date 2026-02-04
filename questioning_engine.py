from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, Optional, Tuple


class State(str, Enum):
    IDLE = "Idle"
    AWARENESS = "Awareness"
    TYPING = "Typing"
    REFINEMENT = "Refinement"
    EXIT = "Exit"


class QuestionType(str, Enum):
    FACT = "FACT"
    JUDGEMENT = "JUDGEMENT"
    VALUE = "VALUE"


@dataclass
class LogEvent:
    state_from: State
    state_to: State
    question_type: Optional[QuestionType] = None
    refinement_attempted: bool = False


Logger = Callable[[LogEvent], None]


@dataclass
class QuestioningEngine:
    state: State = State.IDLE
    question_type: Optional[QuestionType] = None
    refinement_attempted: bool = False
    logger: Optional[Logger] = None
    _refinement_used: bool = field(default=False, init=False)

    def start(self) -> str:
        return self._transition(State.AWARENESS, self._awareness_prompt())

    def handle_input(self, user_input: Optional[str]) -> str:
        if self._is_exit(user_input):
            return self._transition(State.EXIT, self._exit_prompt())

        if self.state == State.AWARENESS:
            return self._transition(State.TYPING, self._typing_prompt(user_input))

        if self.state == State.TYPING:
            return self._transition(State.REFINEMENT, self._refinement_prompt())

        if self.state == State.REFINEMENT:
            return self._transition(State.EXIT, self._exit_prompt())

        return self._transition(State.AWARENESS, self._awareness_prompt())

    def _transition(self, new_state: State, output: str) -> str:
        if self.state != new_state:
            self._log_transition(self.state, new_state)
            self.state = new_state
        return output

    def _log_transition(self, from_state: State, to_state: State) -> None:
        if self.logger is None:
            return
        event = LogEvent(
            state_from=from_state,
            state_to=to_state,
            question_type=self.question_type,
            refinement_attempted=self.refinement_attempted,
        )
        self.logger(event)

    def _is_exit(self, user_input: Optional[str]) -> bool:
        if user_input is None:
            return True
        stripped = user_input.strip()
        if not stripped:
            return True
        exit_terms = {"exit", "quit", "stop", "bye", "no", "不要", "停", "结束"}
        return stripped.lower() in exit_terms

    def _awareness_prompt(self) -> str:
        return (
            "Which one feels closer right now?\n"
            "A. I don’t know what is happening\n"
            "B. I’m not sure if this is right\n"
            "C. I don’t feel okay about the result\n"
            "D. I can’t tell yet"
        )

    def _typing_prompt(self, user_input: Optional[str]) -> str:
        self.question_type = self._classify_question(user_input or "")
        if self.question_type == QuestionType.FACT:
            return (
                "This feels more like a Fact question.\n"
                "Fact questions are about what happened or how something works."
            )
        if self.question_type == QuestionType.JUDGEMENT:
            return (
                "This feels more like a Judgement question.\n"
                "Judgement questions involve what is right or better."
            )
        return (
            "This feels more like a Value question.\n"
            "Value questions involve what matters or what should matter."
        )

    def _refinement_prompt(self) -> str:
        if self._refinement_used:
            return self._exit_prompt()
        self._refinement_used = True
        self.refinement_attempted = True
        prompt, _ = self._refinement_by_type(self.question_type)
        return prompt

    def _exit_prompt(self) -> str:
        return "We can stop here. You can take this question to someone else if you want."

    def _refinement_by_type(
        self, question_type: Optional[QuestionType]
    ) -> Tuple[str, str]:
        if question_type == QuestionType.JUDGEMENT:
            return (
                "Are you asking about the situation itself, or about someone’s choice?",
                "Focus clarification",
            )
        if question_type == QuestionType.VALUE:
            return (
                "Would the question change if one condition were different?",
                "Condition checking",
            )
        return (
            "Are you asking about this situation, or all situations?",
            "Scope narrowing",
        )

    def _classify_question(self, text: str) -> QuestionType:
        lowered = text.lower()
        value_terms = {"fair", "fairness", "meaning", "important", "should matter", "价值"}
        judgement_terms = {"right", "wrong", "better", "worse", "choice", "should i"}
        if any(term in lowered for term in value_terms):
            return QuestionType.VALUE
        if any(term in lowered for term in judgement_terms):
            return QuestionType.JUDGEMENT
        return QuestionType.FACT


def _run_cli() -> None:
    engine = QuestioningEngine()
    print(engine.start())
    while engine.state != State.EXIT:
        try:
            user_input = input("> ")
        except EOFError:
            user_input = ""
        print(engine.handle_input(user_input))


if __name__ == "__main__":
    _run_cli()
