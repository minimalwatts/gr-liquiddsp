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
#include "iir_filter_ccf_impl.h"
#include <liquid/liquid.h>

namespace gr {
  namespace liquiddsp {

    iir_filter_ccf::sptr
    iir_filter_ccf::make(const std::vector<float> &fftaps, const std::vector<float> &fbtaps)
    {
      return gnuradio::get_initial_sptr
        (new iir_filter_ccf_impl(fftaps, fbtaps));
    }

    /*
     * The private constructor
     */
    iir_filter_ccf_impl::iir_filter_ccf_impl(const std::vector<float> &fftaps, const std::vector<float> &fbtaps)
      : gr::sync_block("iir_filter_ccf",
              gr::io_signature::make(1, 1, sizeof(gr_complex *)),
              gr::io_signature::make(1, 1, sizeof(gr_complex *)))
    {

        int nb = fftaps.size();
        int na = fbtaps.size();

        d_iir = iirfilt_crcf_create(const_cast<float *>(&fftaps[0]),nb,const_cast<float *>(&fbtaps[0]),na);

    }

    /*
     * Our virtual destructor.
     */
    iir_filter_ccf_impl::~iir_filter_ccf_impl()
    {
        iirfilt_crcf_destroy((iirfilt_crcf) d_iir);
    }

    int
    iir_filter_ccf_impl::work(int noutput_items,
			  gr_vector_const_void_star &input_items,
			  gr_vector_void_star &output_items)
    {
        const gr_complex *in = (const gr_complex *) input_items[0];
        gr_complex *out = (gr_complex *) output_items[0];

        int count = 0;

        while(count++ < noutput_items) {

            iirfilt_crcf_execute((iirfilt_crcf) d_iir, in[count],&out[count]);

        }

        // Tell runtime system how many output items we produced.
        return noutput_items;
    }

  } /* namespace liquiddsp */
} /* namespace gr */

