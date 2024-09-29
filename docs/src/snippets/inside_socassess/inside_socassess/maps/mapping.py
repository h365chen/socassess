from socassess import userargs


def shared_func(params: str):
    content = (userargs.artifacts / 'test_case_context.txt').open('r')
    filtered_lines = []
    for line in content:
        if params in line:
            filtered_lines.append(line)
    return f"""
{params} passed.

In addition, here are more detail of it:

{''.join(filtered_lines)}
    """.strip()


detail = {
    frozenset([
        'test_it::test_and_provide_context_1::passed',
    ]): {
        'feedback': "Congrats! {content}",
        'function': {
            'name': shared_func,
            'params': 'test_and_provide_context_1',
        }
    },
    frozenset([
        'test_it::test_and_provide_context_2::passed',
    ]): {
        'feedback': "Congrats! {content}",
        'function': {
            'name': shared_func,
            'params': 'test_and_provide_context_2',
        }
    },
}
