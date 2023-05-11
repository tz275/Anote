def prompt_summarize_woking_info(text):
    prompt = f'''
        Your task is to summarize the following text, which is delimited with triple dashes, to the JSON format I provided, which is delimited with triple backticks.
        Then return and only return the JSON String with a translation of all the keys and values in English.
        ---
        {text}
        ---

        ```
        {{position: string,
        company: string,
        is_fulltime: boolean,
        start_date: string,
        end_date: string}}
        ```
        '''
    return prompt

def prompt_email(text):
    prompt = f'''
    Your task is to write an email all in English utilizing the JSON data which is delimited with triple backticks. 
    The email should be sent from a Machine Learning Company called Anote representative, with a proper greeting directed toward the individual's recent working experience.
    Return the email content that is prepared for sending to the intended recipient without the Subject. (Do not include any words like [your name], [your phone], etc. in this email.)

    ```
    {text}
    ```
    '''
    return prompt