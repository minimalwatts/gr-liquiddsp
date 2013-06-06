#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Thu Jun  6 14:36:28 2013
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import liquiddsp
import wx

class top_block(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="Top Block")

		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 32000
		self.fft_size = fft_size = 1024

		##################################################
		# Blocks
		##################################################
		self.wxgui_scopesink2_0 = scopesink2.scope_sink_c(
			self.GetWin(),
			title="Scope Plot",
			sample_rate=samp_rate,
			v_scale=0,
			v_offset=0,
			t_scale=0,
			ac_couple=False,
			xy_mode=False,
			num_inputs=1,
			trig_mode=wxgui.TRIG_MODE_AUTO,
			y_axis_label="Counts",
		)
		self.Add(self.wxgui_scopesink2_0.win)
		self.liquiddsp_fft_1 = liquiddsp.fft(1024, 0, 0)
		self.liquiddsp_fft_0 = liquiddsp.fft(fft_size, 1, 0)
		self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, fft_size)
		self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate)
		self.blocks_sub_xx_0 = blocks.sub_cc(1)
		self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_size)
		self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((1.0/fft_size, ))
		self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 1000, 1, 0)

		##################################################
		# Connections
		##################################################
		self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_vector_0, 0))
		self.connect((self.analog_sig_source_x_0, 0), (self.blocks_throttle_0, 0))
		self.connect((self.blocks_stream_to_vector_0, 0), (self.liquiddsp_fft_0, 0))
		self.connect((self.blocks_throttle_0, 0), (self.blocks_sub_xx_0, 1))
		self.connect((self.blocks_sub_xx_0, 0), (self.wxgui_scopesink2_0, 0))
		self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_multiply_const_vxx_0, 0))
		self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_sub_xx_0, 0))
		self.connect((self.liquiddsp_fft_0, 0), (self.liquiddsp_fft_1, 0))
		self.connect((self.liquiddsp_fft_1, 0), (self.blocks_vector_to_stream_0, 0))


# QT sink close method reimplementation

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
		self.blocks_throttle_0.set_sample_rate(self.samp_rate)
		self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate)

	def get_fft_size(self):
		return self.fft_size

	def set_fft_size(self, fft_size):
		self.fft_size = fft_size
		self.blocks_multiply_const_vxx_0.set_k((1.0/self.fft_size, ))

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = top_block()
	tb.Start(True)
        tb.Wait()

