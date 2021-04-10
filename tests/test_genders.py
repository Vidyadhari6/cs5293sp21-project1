from project1 import redactor
def test_redact_genders():
    text = ['My kid name is Kevin. His birth date is 2021-09-09. His phone number is 989-859-4124.']
    o_text, o_stats = redactor.redact_genders(text, 'test.txt')
    assert len(text)  == len(o_text), "Redaction process unsuccessful"