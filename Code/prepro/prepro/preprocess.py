import glob
import os

from subprocess import call, Popen, PIPE


class Preprocess:

    def __init__(self, utils_folder):
        self.utils_folder = utils_folder

    def tokenize(self, input_file, output_file):
        # Tokenize text from input file and save tokenized result to output file
        call(["mono", os.path.join(self.utils_folder, "preprocessinghr", "PreprocessingHR.exe"),
              input_file, output_file])

        tokenized = []
        # Read tokenized file and put tokens from each sentence in a separate list
        with open(output_file) as f:
            for line in f:
                tokenized.append(line.strip())
        return tokenized

    def pos_tag(self, input_file, output_file):
        # Read lines from input file in one string
        input_text = ''
        with open(input_file) as f:
            for line in f:
                input_text += line

        # Send string with input lines to tagger and save output in a string
        p = Popen([os.path.join(self.utils_folder, "hunpos", "tagger.native"),
                   os.path.join(self.utils_folder, "hunpos", "cc-by-sa.hunpos")],
                  stdin=PIPE, stdout=PIPE)
        output = p.communicate(input=input_text)[0]

        hunpos_tags = []
        # Write tagged lines in output file with token and tag separated by '/'
        # Add lines to a list to be returned (token and tag separated by TAB)
        with open(output_file, 'a') as f:
            for output_line in output.split('\n'):
                hunpos_tags.append(tuple(output_line.strip().split('\t')))
                line = '/'.join(output_line.strip().split('\t'))
                f.write('%s\n' % line)
        return hunpos_tags

    def lemmatize(self, input_file, output_file):
        # Split input text into sentences
        hunpos_sents = []
        with open(input_file) as f:
            sent = []
            for line in f:
                if line.strip() != '':
                    sent.append(line.strip())
                elif len(sent) > 0:
                    hunpos_sents.append(sent)
                    sent = []

        cst_lemmas = []
        # Go through list of sentences and lemmatize each sentence separately
        # (if sentences are lemmatized together, output doesn't contain empty lines between sentences)
        sent_num = len(hunpos_sents)
        for i in range(sent_num):
            sent = hunpos_sents[i]
            input_text = '\n'.join(sent)

            # Saving POS-tagged sentence in a separate file
            with open(input_file + str(i), 'a') as f:
                f.write('%s' % input_text)
            call([os.path.join(self.utils_folder, "cstlemmatizer", "cstlemmatizer"), "-eU", "-f",
                  os.path.join(self.utils_folder, "cstlemmatizer", "setimes.hr.v1.2.manual.cstpats"), "-d",
                  os.path.join(self.utils_folder, "cstlemmatizer", "setimes.hr.v1.2.manual.cstdict"), "-i",
                  input_file + str(i), "-o", output_file + str(i)])

            # Collect all lemmas in one list
            with open(output_file + str(i)) as fd:
                for line in fd:
                    line_elems = line.strip().split('\t')
                    cst_lemmas.append(line_elems[1])
                cst_lemmas.append('')
        return cst_lemmas

    def dep_parse(self, input_file, output_file):
        call(["java", "-cp", os.path.join(self.utils_folder, "mstparser", "output", "classes") + ":" +
              os.path.join(self.utils_folder, "mstparser", "lib", "trove.jar"),
              "-Xmx6000m", "mstparser.DependencyParser",
              "test", "model-name:" + os.path.join(self.utils_folder, "mstparser", "model.mte5.defnpout"),
              "test-file:" + input_file, "output-file:" + output_file, "format:CONLL"])

    def pos_lemmatize(self, text):
        prepro_temp_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'temp_dir')
        if not os.path.exists(prepro_temp_dir):
            os.makedirs(prepro_temp_dir)

        input_file = os.path.join(prepro_temp_dir, 'temp_text_input')
        with open(input_file, 'w') as f:
            f.write('%s\n' % text)

        tokenizer_output_file = os.path.join(prepro_temp_dir, 'temp_token_out')
        self.tokenize(input_file, tokenizer_output_file)

        pos_output_file = os.path.join(prepro_temp_dir, 'temp_pos_out')
        pos_lines = self.pos_tag(tokenizer_output_file, pos_output_file)

        lemmatizer_output_file = os.path.join(prepro_temp_dir, 'temp_cst_out')
        lemma_lines = self.lemmatize(pos_output_file, lemmatizer_output_file)

        for file_name in glob.glob(os.path.join(prepro_temp_dir, 'temp_*')):
            os.remove(file_name)
        return pos_lines, lemma_lines
