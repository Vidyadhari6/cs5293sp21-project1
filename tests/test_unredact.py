from project1 import unredactor
def test_redact_phones():
    text = ['My kid name is Kevin. His birth date is 2021-09-09. His phone number is 989-859-4124.']
    o_dict = unredactor.find_entity(text, 'test.txt')
    assert type(o_dict) == list "test find entity successful"