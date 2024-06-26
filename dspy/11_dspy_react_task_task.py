import dspy
from dspy.teleprompt import LabeledFewShot

from dspy_utils import BOLD_BEGIN, BOLD_END, ThoughtReflection
from dspy_examples_utils import get_few_shot_dspy_examples

import warnings
warnings.filterwarnings("ignore")

    
if __name__ == "__main__":
    # Setup OLlama environment on the local machine
    ollama_mistral = dspy.OllamaLocal(model='mistral',
                                        max_tokens=5000)
    # Instantiate the ColBERTv2 as Retrieval module
    colbert_rm = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')

    # Configure the settings
    dspy.settings.configure(lm=ollama_mistral, rm=colbert_rm)

    # Get some few-shot DSPy Examples
    examples_set = get_few_shot_dspy_examples()

    # Instantiate the ThoughtReflection module
    tought_of_reflection = ThoughtReflection()

    # Set up a basic teleprompter optimizer 
    # and use it to compile our ReACT program.
    teleprompter = LabeledFewShot(k=5)

    # Compile the ReACT model
    compiled_tf= teleprompter.compile(tought_of_reflection, trainset=examples_set)

    # Question to ask the compile and optimized ReACT model
    answer = compiled_tf("""Based on information provided to you upto 2023, 
                            what is the elevation in feet of Mount Kilimanjoro?
                            What is the recommended and healthy way to climb the mountain 
                            in terms of ascending number of feet per day?
                            and how long will it take to get to the top?
""")
    # Print the answer
    print(f"{BOLD_BEGIN}Answer    : {BOLD_END}{answer}")

    # Examine the history of the prompts generated by the ReACT model
    print("------LLM prompts history of the last question------")
    print(ollama_mistral.inspect_history(n=1))