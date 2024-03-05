jas_image_t *jp2_decode(jas_stream_t *in, const char *optstr)
{
	jp2_box_t *box;
	int found;
	jas_image_t *image;
	jp2_dec_t *dec;
	bool samedtype;
	int dtype;
	unsigned int i;
	jp2_cmap_t *cmapd;
	jp2_pclr_t *pclrd;
	jp2_cdef_t *cdefd;
	unsigned int channo;
	int newcmptno;
	int_fast32_t *lutents;
error:
	if (box) {
		jp2_box_destroy(box);
	}
	if (dec) {
		jp2_dec_destroy(dec);
	}
	return 0;
}