import anthropic
import pandas as pd
import string


def main():

    trans_table = str.maketrans('', '', string.punctuation)

    for psalm_num in range(1,151):


        client = anthropic.Anthropic()

        input = """
Based only on your knowledge of Ancient Greek, translate the following passage. Do not attempt to recognize the source of the passage:
Ancient Greek:
1.	ρηματα εκκλησιαστου υιου δαυιδ βασιλεως ισραηλ εν ιερουσαλημ
2.	ματαιοτης ματαιοτητων ειπεν ο εκκλησιαστης ματαιοτης ματαιοτητων τα παντα ματαιοτης
3.	τις περισσεια τω ανθρωπω εν παντι μοχθω αυτου ω μοχθει υπο τον ηλιον
4.	γενεα πορευεται και γενεα ερχεται και η γη εις τον αιωνα εστηκεν
5.	και ανατελλει ο ηλιος και δυνει ο ηλιος και εις τον τοπον αυτου ελκει
Line-by-line English translations:
1.	The words of the Preacher, the son of David, king of Israel in Jerusalem. 
2.	Vanity of vanities, said the Preacher, vanity of vanities; all is vanity. 
3.	What advantage is there to a man in all his labor that he takes under the sun? 
4.	A generation goes, and a generation comes: but the earth stands for ever. 
5.	And the sun arises, and the sun goes down and draws toward its place.
Ancient Greek: \n"""


        psalm = pd.read_csv('Hebrew_num_CSVs/Psalm_'+str(psalm_num)+'.csv')

        for num, verse in enumerate(list(psalm['Septuagint'])):
            verse_str = verse.translate(trans_table)
            input += str(num+1) + '\t' + verse_str + '\n'

        input += "Line-by-line English translations: \n"

        # print(input)

        max_t = 1000
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
        translation_df.to_csv('claude_translations/Septuagint_'+str(psalm_num)+'.csv')


if __name__ == '__main__':
    main()