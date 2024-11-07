def count_if(function: callable, phrases: tuple | list) -> int:
    return sum(1 for phrase in phrases if function(phrase))
