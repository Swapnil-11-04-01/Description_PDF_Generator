# Approach

My approach is simple, first my program will take an input from the user.
Then it will use a llm model from huggingface to generate its description.
I asked few questions in a prompt to generate longer description.
Then same llm model will translate enf text to french.
Then I have used another model from huggingface for ai image generation.
After all the generation, pdf will be generate and saved in artifact.

# Challanges

I didn't had the openai account so used hugging face models.
Since huggingface models are lightweight, they generate short and not so accurate results.
My PC dont have Nvidia GPU so couldnt not run and test the code locally, that's why used google colab for complete execution and generation of demo file.

# Attachments

Find demo pdf named as "photosynthesis".
Also find a jupyter notebook with execution