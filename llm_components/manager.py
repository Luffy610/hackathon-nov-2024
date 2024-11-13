import logging
import pandas as pd
from llmx import llm, TextGenerationConfig
from llm_components.goal_generator import GoalGenerator
from llm_components.summarizer import Summarizer
from utils.datamodels import Summary, Persona, Goal
from typing_extensions import List

logger = logging.getLogger("manager")
class Manager:

    def __init__(self, text_gen):

        self.text_gen = text_gen or llm()
        self.summarizer = Summarizer()
        self.goal = GoalGenerator()
        self.data = None

    def check_textgen(self, config: TextGenerationConfig):
        if config.provider is None:
            config.provider = self.text_gen.provider or "openai"
            logger.info("Provider is not set, using default provider - %s", config.provider)
            return

        if self.text_gen.provider != config.provider:
            logger.info(
                "Switching Text Generator Provider from %s to %s",
                self.text_gen.provider,
                config.provider)
            self.text_gen = llm(provider=config.provider)

    def summarize(self,
                  data: pd.DataFrame,
                  file_name="",
                  n_samples: int = 3,
                  summary_method: str = "default",
                  text_gen_config: TextGenerationConfig = TextGenerationConfig(n=1, temperature=0),
                  ) -> Summary:
        self.check_textgen(config=text_gen_config)

        self.data = data

        return self.summarizer.summarize(data=self.data,
                                         text_gen=self.text_gen,
                                         file_name=file_name,
                                         n_samples=n_samples,
                                         summary_method=summary_method,
                                         text_gen_config=text_gen_config)



    def goals(self,
              summary: Summary = None,
              data: pd.DataFrame = None,
              file_name = "",
              n_samples: int = 3,
              summary_method: str = "default",
              text_gen_config: TextGenerationConfig = TextGenerationConfig(),
              no_of_goals = 5,
              persona: Persona = None
              ) -> List[Goal]:
        self.check_textgen(config=text_gen_config)

        if isinstance(persona, dict):
            persona = Persona(**persona)

        if isinstance(persona, str):
            persona = Persona(persona=persona, rationale="")

        if summary is None:
            summary = self.summarize(data=data,
                                     file_name=file_name,
                                     n_samples=n_samples,
                                     summary_method=summary_method,
                                     text_gen_config=text_gen_config,
                                     )

        return self.goal.generate(summary=summary,
                                  text_gen=self.text_gen,
                                  text_config=text_gen_config,
                                  no_of_goals=no_of_goals,
                                  persona=persona
                                  )