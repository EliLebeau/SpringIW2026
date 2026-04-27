# produce machine translations of Hebrew text

import anthropic
import pandas as pd


def main():
    for psalm_num in range (1,151):
        client = anthropic.Anthropic()

        input = """
Based only on your knowledge of Biblical Hebrew, translate the following passage. Do not attempt to recognize the source of the passage:
Hebrew: 
1.	דברי קהלת בן־דוד מלך בירושלם
2.	הבל הבלים אמר קהלת הבל הבלים הכל הבל
3.	מה־יתרון לאדם בכל־עמלו שיעמל תחת השמש
4.	דור הלך ודור בא והארץ לעולם עמדת
5.	וזרח השמש ובא השמש ואל־מקומו שואף זורח הוא שם
Line-by-line English translations:
1.	The words of Koheleth, the son of David, king in Jerusalem. 
2.	Vanity of vanities, said Koheleth; vanity of vanities, all is vanity. 
3.	What profit has man of all his labor wherein he labors under the sun? 
4.	One generation passes away, and another generation comes; and the earth abides forever. 
5.	The sun also arises, and the sun goes down, and hastens to his place where he arises.
Hebrew: \n"""


        psalm = pd.read_csv('Hebrew_num_CSVs/Psalm_'+str(psalm_num)+'.csv')

        for num, verse in enumerate(list(psalm['Hebrew'])):
            input += str(num+1) + '\t' + verse + '\n'

        input += "Line-by-line English translations: \n"


        max_t = 1000

        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=max_t,
            messages=[
                {
                    "role": "user",
                    "content": input,
                }
            ],
        )
        print(message.content)
        print()
        print(message.content[0].text)
        print()

        translation = message.content[0].text.split('\n')
        final_text = []
        for verse in translation:
            final_text.append(' '.join(verse.split(' ')[1:]))

        translation_df = pd.DataFrame({'text' : final_text})
        translation_df.to_csv('claude_translations/Hebrew_'+str(psalm_num)+'.csv')


if __name__ == '__main__':
    main()