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


#ifndef INCLUDED_LIQUIDDSP_FFT_H
#define INCLUDED_LIQUIDDSP_FFT_H

#include <liquiddsp/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace liquiddsp {

    /*!
     * \brief <+description of block+>
     * \ingroup liquiddsp
     *
     */
    class LIQUIDDSP_API fft : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<fft> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of liquiddsp::fft.
       *
       * To avoid accidental use of raw pointers, liquiddsp::fft's
       * constructor is in a private implementation
       * class. liquiddsp::fft::make is the public interface for
       * creating new instances.
       */
      static sptr make(unsigned int size, int forward, int flags);
    };

  } // namespace liquiddsp
} // namespace gr

#endif /* INCLUDED_LIQUIDDSP_FFT_H */

