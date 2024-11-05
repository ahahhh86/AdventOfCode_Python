def count_if(function: callable, phrases: tuple) -> int:
    return sum(1 for phrase in phrases if function(phrase))
