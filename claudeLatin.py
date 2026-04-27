import anthropic
import pandas as pd
import string


def main():

    trans_table = str.maketrans('', '', string.punctuation)

    for psalm_num in range(1,151):

        # if psalm_num == 119:
        #     continue

        client = anthropic.Anthropic()

        input = """
Based only on your knowledge of Latin, translate the following passage. Do not attempt to recognize the source of the passage:
Latin: 
1.	verba Ecclesiastes filii David regis Hierusalem
2.	vanitas vanitatum dixit Ecclesiastes vanitas vanitatum omnia vanitas
3.	quid habet amplius homo de universo labore suo quod laborat sub sole
4.	generatio praeterit et generatio advenit terra vero in aeternum stat
5.	oritur sol et occidit et ad locum suum revertitur ibique renascens
Line-by-line English translations:
1.	The words of Ecclesiastes, the son of David, king of Jerusalem.
2.	Vanity of vanities, said Ecclesiastes: vanity of vanities, and all is vanity.
3.	What has a man more of all his labor, that he takes under the sun?
4.	One generation passes away, and another generation comes: but the earth stands forever.
5.	The sun rises, and goes down, and returns to his place: and there rising again.
Latin: \n"""


        psalm = pd.read_csv('Hebrew_num_CSVs/Psalm_'+str(psalm_num)+'.csv')

        for num, verse in enumerate(list(psalm['Hebrew Psalter'])):
            verse_str = verse.translate(trans_table)
            input += str(num+1) + '\t' + verse_str + '\n'

        input += "Line-by-line English translations: \n"

        print(input)

        max_t = 1000
        # if psalm_num == 37 or psalm_num == 68:
        #     max_t = 1500
        # if psalm_num == 18 or psalm_num == 78 or psalm_num == 89 or psalm_num == 106:
        #     max_t = 2000

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
        translation_df.to_csv('claude_translations/Hebrew_Psalter_'+str(psalm_num)+'.csv')


if __name__ == '__main__':
    main()