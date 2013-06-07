#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Fri Jun  7 11:03:08 2013
##################################################

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import PyQt4.Qwt5 as Qwt
import liquiddsp
import sip
import sys

class top_block(gr.top_block, Qt.QWidget):

	def __init__(self):
		gr.top_block.__init__(self, "Top Block")
		Qt.QWidget.__init__(self)
		self.setWindowTitle("Top Block")
		try:
		     self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
		except:
		     pass
		self.top_scroll_layout = Qt.QVBoxLayout()
		self.setLayout(self.top_scroll_layout)
		self.top_scroll = Qt.QScrollArea()
		self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
		self.top_scroll_layout.addWidget(self.top_scroll)
		self.top_scroll.setWidgetResizable(True)
		self.top_widget = Qt.QWidget()
		self.top_scroll.setWidget(self.top_widget)
		self.top_layout = Qt.QVBoxLayout(self.top_widget)
		self.top_grid_layout = Qt.QGridLayout()
		self.top_layout.addLayout(self.top_grid_layout)

		self.settings = Qt.QSettings("GNU Radio", "top_block")
		self.restoreGeometry(self.settings.value("geometry").toByteArray())


		##################################################
		# Variables
		##################################################
		self.variable_frequency = variable_frequency = 1e3
		self.samp_rate = samp_rate = 32000

		##################################################
		# Blocks
		##################################################
		self._variable_frequency_layout = Qt.QVBoxLayout()
		self._variable_frequency_tool_bar = Qt.QToolBar(self)
		self._variable_frequency_layout.addWidget(self._variable_frequency_tool_bar)
		self._variable_frequency_tool_bar.addWidget(Qt.QLabel("Frequency"+": "))
		self._variable_frequency_counter = Qwt.QwtCounter()
		self._variable_frequency_counter.setRange(0, samp_rate/2, 100)
		self._variable_frequency_counter.setNumButtons(2)
		self._variable_frequency_counter.setValue(self.variable_frequency)
		self._variable_frequency_tool_bar.addWidget(self._variable_frequency_counter)
		self._variable_frequency_counter.valueChanged.connect(self.set_variable_frequency)
		self._variable_frequency_slider = Qwt.QwtSlider(None, Qt.Qt.Horizontal, Qwt.QwtSlider.BottomScale, Qwt.QwtSlider.BgSlot)
		self._variable_frequency_slider.setRange(0, samp_rate/2, 100)
		self._variable_frequency_slider.setValue(self.variable_frequency)
		self._variable_frequency_slider.setMinimumWidth(200)
		self._variable_frequency_slider.valueChanged.connect(self.set_variable_frequency)
		self._variable_frequency_layout.addWidget(self._variable_frequency_slider)
		self.top_layout.addLayout(self._variable_frequency_layout)
		self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
			32768, #size
			samp_rate, #samp_rate
			"QT GUI Plot", #name
			2 #number of inputs
		)
		self.qtgui_time_sink_x_0.set_update_time(0.10)
		self.qtgui_time_sink_x_0.set_y_axis(-1, 1)
		self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
		self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
		self.liquiddsp_iir_filter_ccf_0 = liquiddsp.iir_filter_ccf(([0.009132988623707152, 0.012299865438686611, 0.0201534813784915, 0.02015348137849149, 0.01229986543868664, 0.009132988623707162]), ([1.0, -3.1085232431111423, 4.682509078805568, -3.9933767097618924, 1.9198236423390123, -0.41726009738977526]))
		self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate)
		self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, variable_frequency, 1, 0)

		##################################################
		# Connections
		##################################################
		self.connect((self.analog_sig_source_x_0, 0), (self.blocks_throttle_0, 0))
		self.connect((self.blocks_throttle_0, 0), (self.liquiddsp_iir_filter_ccf_0, 0))
		self.connect((self.liquiddsp_iir_filter_ccf_0, 0), (self.qtgui_time_sink_x_0, 1))
		self.connect((self.analog_sig_source_x_0, 0), (self.qtgui_time_sink_x_0, 0))


# QT sink close method reimplementation
	def closeEvent(self, event):
		self.settings = Qt.QSettings("GNU Radio", "top_block")
		self.settings.setValue("geometry", self.saveGeometry())
		event.accept()

	def get_variable_frequency(self):
		return self.variable_frequency

	def set_variable_frequency(self, variable_frequency):
		self.variable_frequency = variable_frequency
		self._variable_frequency_counter.setValue(self.variable_frequency)
		self._variable_frequency_slider.setValue(self.variable_frequency)
		self.analog_sig_source_x_0.set_frequency(self.variable_frequency)

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
		self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
		self.blocks_throttle_0.set_sample_rate(self.samp_rate)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	qapp = Qt.QApplication(sys.argv)
	tb = top_block()
	tb.start()
	tb.show()
	qapp.exec_()
	tb.stop()
	tb = None #to clean up Qt widgets

