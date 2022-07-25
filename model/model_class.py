import torch.nn as nn
from transformers import BertModel


class BertClassifier(nn.Module):
    def __init__(self, model_name, linear_size, num_class):
        super(BertClassifier, self).__init__()

        self.bert = BertModel.from_pretrained(model_name)
        self.dropout1 = nn.Dropout(p=self.bert.config.hidden_dropout_prob)
        self.linear1 = nn.Linear(in_features=768, out_features=linear_size)
        self.batch_norm1 = nn.BatchNorm1d(num_features=linear_size)
        self.dropout2 = nn.Dropout(p=0.75)
        self.linear2 = nn.Linear(in_features=linear_size, out_features=num_class)
        self.sigmoid = nn.Sigmoid()

    def forward(self, input_ids, attention_mask, token_type_ids=None):
        outputs = self.bert(
            input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids
        )
        x = self.dropout1(outputs[1])
        x = self.linear1(x)
        x = self.dropout2(x)
        x = self.batch_norm1(x)
        x = self.linear2(x)
        return self.sigmoid(x)
