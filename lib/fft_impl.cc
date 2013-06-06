/* -*- c++ -*- */
/* 
 * Copyright 2013 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "fft_impl.h"
#include <liquid/liquid.h>

namespace gr {
  namespace liquiddsp {

	fft::sptr
	fft::make(unsigned int size, int forward, int flags)
	{
	return gnuradio::get_initial_sptr
	  (new fft_impl(size, forward, flags));
	}

	/*
	* The private constructor
	*/
	fft_impl::fft_impl(unsigned int size, int forward, int flags)
	: gr::sync_block("fft",
			gr::io_signature::make(1, 1, size * sizeof(gr_complex)),
			gr::io_signature::make(1, 1, size * sizeof(gr_complex)))
	{
		// Make sure liquid complex type matches gnu radio complex type in size
		assert (sizeof (float complex) == sizeof (gr_complex));

		// Copy actual parameters to block variables
		d_forward = forward;
		d_size = size;
		d_flags = flags; // not used

		// Create input and output buffers
		d_inbuf = (gr_complex *) malloc (sizeof (gr_complex) * size);
		d_outbuf = (gr_complex *) malloc (sizeof (gr_complex) * size);

		// Define FFT plan with liquid
		d_fft = fft_create_plan(	size,
									d_inbuf,  /* liquid uses std::complex and gr_complex is std::complex<float> */
									d_outbuf,
									forward ? LIQUID_FFT_FORWARD : LIQUID_FFT_BACKWARD,
									flags);
	}

	/*
	* Our virtual destructor.
	*/
	fft_impl::~fft_impl()
	{
		fft_destroy_plan((fftplan) d_fft);
	}

	int
	fft_impl::work(int noutput_items,
			  gr_vector_const_void_star &input_items,
			  gr_vector_void_star &output_items)
	{
	  const gr_complex *in = (const gr_complex *) input_items[0];
	  gr_complex *out = (gr_complex *) output_items[0];

	  unsigned int input_data_size = input_signature()->sizeof_stream_item (0);
	  unsigned int output_data_size = output_signature()->sizeof_stream_item (0);

	  int count = 0;

	  while(count++ < noutput_items) {
		// Load data from buffer into local array (with FFT shifting)
			if(!d_forward) {  // apply an ifft shift on the data
				unsigned int len = (unsigned int)(floor(d_size/2.0)); // half length of complex array
				memcpy(&d_inbuf[0], &in[len], sizeof(gr_complex)*(d_size - len));
				memcpy(&d_inbuf[d_size - len], &in[0], sizeof(gr_complex)*len);
			}
			else {
				memcpy(d_inbuf, in, input_data_size);
			}

			// Compute the fft
			fft_execute((fftplan) d_fft);

			// Copy result to our output
			if(d_forward) {  // apply a fft shift on the data
			  unsigned int len = (unsigned int)(ceil(d_size/2.0));
			  memcpy(&out[0], &d_outbuf[len], sizeof(gr_complex)*(d_size - len));
			  memcpy(&out[d_size - len], &d_outbuf[0], sizeof(gr_complex)*len);
			}
			else {
			  memcpy (out, d_outbuf, output_data_size);
			}

			in  += d_size;
			out += d_size;

	  }

	  // Tell runtime system how many output items we produced.
	  return noutput_items;
	}
  } /* namespace liquiddsp */
} /* namespace gr */

