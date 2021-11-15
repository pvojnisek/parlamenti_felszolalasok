from spacy.util import minibatch, compounding
import csv
import random
import sys
import hu_core_ud_lg


def evaluate(tokenizer, textcat, texts, cats):
    docs = (tokenizer(text) for text in texts)
    tp = 0.0  # True positives
    fp = 1e-8  # False positives
    fn = 1e-8  # False negatives
    tn = 0.0  # True negatives
    for i, doc in enumerate(textcat.pipe(docs)):
        gold = cats[i]
        for label, score in doc.cats.items():
            if label not in gold:
                continue
            if label == "Kormány":
                continue
            if score >= 0.5 and gold[label] >= 0.5:
                tp += 1.0
            elif score >= 0.5 and gold[label] < 0.5:
                fp += 1.0
            elif score < 0.5 and gold[label] < 0.5:
                tn += 1
            elif score < 0.5 and gold[label] >= 0.5:
                fn += 1
    print(tp, tn, fp, fn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    if (precision + recall) == 0:
        f_score = 0.0
    else:
        f_score = 2 * (precision * recall) / (precision + recall)
    return {"textcat_p": precision, "textcat_r": recall, "textcat_f": f_score}


random.seed(42)

csv.field_size_limit(sys.maxsize)
csvin = open('preprocessed.csv', 'r', newline='', encoding='utf-8')
csvreader = csv.DictReader(csvin, lineterminator='\n')
data = [row for row in csvreader]
# print(data[0])

parties = ['Fidesz', 'Jobbik', 'KDNP', 'MSZP', 'LMP']

opposition = ['Jobbik', 'MSZP', 'LMP', 'DK', 'Párbeszéd']
ruleing = ['Fidesz', 'KDNP']

felsz_by_party = dict()
data = [f for f in data if f['party'] in opposition or f['party'] in ruleing]
parties = ['Ellenzék', 'Kormány']
felsz_by_party['Ellenzék'] = [{'cat': {'Ellenzék': f['party'] in opposition, 'Kormány': f['party'] in ruleing
                                       }, 'text': f['text']} for f in data if f['party'] in opposition]
felsz_by_party['Kormány'] = [{'cat': {'Ellenzék': f['party'] in opposition, 'Kormány': f['party'] in ruleing
                                      }, 'text': f['text']} for f in data if f['party'] in ruleing]

minlen = min([len(felsz_by_party[p]) for p in parties])
for party in parties:
    random.shuffle(felsz_by_party[party])
    felsz_by_party[party] = felsz_by_party[party][:minlen]

# print(felsz_by_party[parties[0]][0])

splitat = int(minlen*0.7)
felsz_by_party_train = dict()
felsz_by_party_eval = dict()
for party in parties:
    felsz_by_party_train[party] = felsz_by_party[party][:splitat]
    felsz_by_party_eval[party] = felsz_by_party[party][splitat:]

nlp = hu_core_ud_lg.load()

print(parties)

textcat = nlp.create_pipe(
    "textcat", config={"exclusive_classes": True, "architecture": "simple_cnn"})
nlp.add_pipe(textcat, last=True)

train_data = list()

eval_data = list()
for party in parties:
    eval_data += felsz_by_party_eval[party]

random.shuffle(eval_data)

text_eval = [f['text'] for f in eval_data]
cat_eval = [f['cat'] for f in eval_data]

for party in parties:
    train_data += [(f['text'], {
        'cats': f['cat']}) for f in felsz_by_party_train[party]]

for party in parties:
    textcat.add_label(party)


print(
    f'train data length: {len(train_data)}, eval data length: {len(text_eval)}')

random.shuffle(train_data)
# print(train_data[:10])
n_iter = 30

other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'textcat']
with nlp.disable_pipes(*other_pipes):  # only train textcat
    optimizer = nlp.begin_training()
    print("Training the model...")
    for i in range(n_iter):
        n = 0
        print(f'{i}. iteration')
        losses = {}
        random.shuffle(train_data)
        batches = minibatch(train_data, size=compounding(4, 32, 1.001))
        for batch in batches:
            texts, annotations = zip(*batch)
            nlp.update(texts, annotations, sgd=optimizer,
                       drop=0.2, losses=losses)
            sys.stdout.write(f"\r{n}. batch {losses['textcat']}")
            n += 1
        print()
        with textcat.model.use_params(optimizer.averages):
            # evaluate on the dev data split off in load_data()
            print('evaluating...')
            scores = evaluate(nlp.tokenizer, textcat,
                              text_eval, cat_eval)
            print(
                "{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}".format(  # print a simple table
                    losses["textcat"],
                    scores["textcat_p"],
                    scores["textcat_r"],
                    scores["textcat_f"],
                )
            )
            print('saving to disk...')
            nlp.to_disk('model')
            print('saving done')

    with nlp.use_params(optimizer.averages):
        nlp.to_disk('model')
