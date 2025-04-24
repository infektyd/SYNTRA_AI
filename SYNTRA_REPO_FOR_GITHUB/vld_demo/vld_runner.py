import os

def interpret_symbol(symbol):
    return {
        '⊕': 'Add condition:',
        '⊖': 'Subtract condition:',
        '↯': 'Detected drift in:',
        '→': 'Leads to:',
        '⚠': 'Warning:',
        '⛔': 'Confirmed fault:'
    }.get(symbol, symbol)

def run_vld(filename):
    print(f"Running VLD script: {filename}\n")
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(' ')
            output = []
            for part in parts:
                if part and part[0] in '⊕⊖↯→⚠⛔':
                    output.append(interpret_symbol(part[0]) + ' ' + part[1:])
                else:
                    output.append(part)
            print(' '.join(output))

if __name__ == '__main__':
    script_path = os.path.join(os.path.dirname(__file__), 'test.vld')
    run_vld(script_path)

