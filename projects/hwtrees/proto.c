
// C implementation of a hardware peripheral
// that can evaluate decision tree ensembles, such as Random Forests etc

typedef hwtrees_address uint16_t;
typedef hwtrees_size uint16_t;
#define HWTREES_NODE_SIZE 3

#define HWTREES_TREES_MAX 32
#define HWTREES_INPUTS_MAX 127

// strict limit for uint16_t addresses. 2**16 // 3 = 21854
#define HWTREES_NODES_MAX 4000

// Dummy RAM in memory
// Would normally be external RAM on SPI bus, share with microprocessor
#define RAM_SIZE 2**16
static uint8_t g_ram = [RAM_SIZE];

int
ram_read(hwtrees_address addr, uint8_t *values, hwtrees_size length)
{
    const int end = addr + length;
    if (end >= RAM_SIZE) {
        return -1;
    }
    memcpy((void *)values, (void *)(g_ram+addr), length);

    return 0;
}

int
ram_write(hwtrees_address addr, uint8_t *values, hwtrees_size length)
{
    const int end = addr + length;
    if (end >= RAM_SIZE) {
        return -1;
    }

    memcpy((void *)(g_ram+addr), (void *)values, length);

    return 0;
}



// Memory representation of the hwtrees memory-mapped peripheral
typedef struct __attribute__((packed, aligned(4))) _hwtrees_register {

    // TODO: maybe add a status register? Use to communicate failures

    hwtrees_address input_start;
    uint8_t input_length;

    hwtrees_address output_start;
    uint8_t output_length;

    hwtrees_address roots_start;
    uint8_t roots_length;

    hwtrees_address nodes_start;
    hwtrees_size nodes_length;

} hwtrees_register;

int
hwtrees_run(hwtrees_register *reg)
{
    // Check max lengths for input, output, roots
    if (reg->input_length > HWTREES_INPUTS_MAX) {
        return -1;
    }

    if (reg->output_length > HWTREES_TREES_MAX) {
        return -1;
    }

    if (reg->roots_length > HWTREES_TREES_MAX) {
        return -1;
    }

    if (reg->roots_length != output_length) {
        return -1;
    }
   
    // FIXME: check that input/output/roots/nodes regions do not overlap

    uint8_t inputs[reg->input_length];
    uint8_t roots[reg->roots_length];
    uint8_t outputs[reg->output_length];

    // FIXME: check RAM reads

    // Read input data
    ram_read(reg->input_start, &inputs, reg->input_length);

    
    // Read roots
    ram_read(reg->roots_start, &roots, reg->roots_length);


    for (int tree=0; tree<reg->roots_length; tree++) {
        uint8_t node[HWTREES_NODE_SIZE];
        uint8_t node_idx = roots[tree];

        while (true) {
            // Read the node
            // FIXME: check for node out-of-bounds
            const hwtrees_address root_addr = \
                reg->nodes_start + (node_idx * HWTREES_NODE_SIZE);
            ram_read(root_addr, &node, HWTREES_NODE_SIZE);

            // Parse the node
            // lowest bit is leaf marker
            // upper bits are the value
            const bool is_leaf = (node[0] & 1);
            const uint8_t feature = node[0] >> 1;
            // Next bytes has decision threshold and what comes next,
            // either a leaf index, or a decision node jump
            const uint8_t threshold = node[1];
            const uint8_t next_value = node[2];

            if (is_leaf) {
                outputs[tree] = next_value;
                break;
            }

            // Is decision node
            if (feature >= reg->input_length) {
                return -1;
            }

            const uint8_t value = input[feature];

            // check the decision node
            if (value >= threshold) {
                node_idx += next_value;
            } else {
                node_idx += 1;
            }
        }
    }

    // Actually write outputs
    ram_write(reg->output_start, outputs, reg->output_length);
}

// Memory representation of the hwtrees memory-mapped peripheral
typedef struct __attribute__((packed, aligned(4))) _hwtrees_node {
    uint8_t is_leaf: 1;
    uint8_t feature: 7;
    int8_t threshold: 7;
    uint8_t next_value: 7;
} hwtrees_node;



void
test_xor_single_tree() {

    const hwtrees_address input_addr = 0x10;
    const hwtrees_address output_addr = 0x20;
    const hwtrees_address roots_addr = 0x30;
    const hwtrees_address nodes_addr = 0x40;

    // FIXME: set up and copy nodes
    n_nodes = 

    hwtrees_register reg = {
        input_addr, 2,
        output_addr, 1,
        roots_addr, 2,
        nodes_addr, n_nodes
    }

    // FIXME: setup and copy roots

    // Test data
    uint8_t test_data[4][2+1] = {
        // in1, in2 -> out 
        { 0,      0,  0 },
        { 255,  255,  0 },
        { 0,    255,  1 },
        { 255,  0,    1 },
    };

    // FIXME: copy inputs
    // FIXME: run the thing, and verify output

}


int void(const char *argv, const int argc) {

     test_xor_single_tree()
    
    
}
