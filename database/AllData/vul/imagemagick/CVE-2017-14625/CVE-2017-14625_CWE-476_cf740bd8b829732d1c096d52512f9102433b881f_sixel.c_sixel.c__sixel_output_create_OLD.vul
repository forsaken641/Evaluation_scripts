sixel_output_t *sixel_output_create(Image *image)
{
    sixel_output_t *output;

    output = (sixel_output_t *) AcquireQuantumMemory(sizeof(sixel_output_t) + SIXEL_OUTPUT_PACKET_SIZE * 2, 1);
    output->has_8bit_control = 0;
    output->save_pixel = 0;
    output->save_count = 0;
    output->active_palette = (-1);
    output->node_top = NULL;
    output->node_free = NULL;
    output->image = image;
    output->pos = 0;

    return output;
}
