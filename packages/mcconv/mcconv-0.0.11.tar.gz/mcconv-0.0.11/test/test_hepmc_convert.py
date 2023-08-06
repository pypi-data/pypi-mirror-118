from mcconv import GenericTextReader, UnparsedTextEvent, hepmc_convert

import os
import unittest
from mcconv import detect_mc_type, McFileTypes
from pyHepMC3 import HepMC3 as hm


class TestGenericTextReader(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def _data_path(self, file_name):
        """Gets data file path"""
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(dir_path, 'data', file_name)

    def _tmp_path(self, file_name):
        """Gets output temporary file path"""

        return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tmp', file_name)

    def test_convert_lund_gemc(self):
        """Test detecting BeaGLE file type"""

        # Beam particles in px, py, pz, e, pid
        beams = [
            (0, 0, -5., 5., 11),
            (0, 0, 110., 110., 2212),
        ]

        hepmc_convert(self._data_path('gemc-lund.3evt.txt'),
                      self._tmp_path('lund-convert.hepmc'),
                      McFileTypes.LUND_GEMC,
                      beam_particles=beams)

        inputA = hm.ReaderAscii(self._tmp_path('lund-convert.hepmc'))
        if inputA.failed():
            raise "inputA.failed()"

        evt = hm.GenEvent()
        inputA.read_event(evt)
        vtx: hm.GenVertex = evt.vertices()[0]
        particle: hm.GenParticle = vtx.particles_out()[0]
        self.assertAlmostEqual(-4.457052e+00, particle.momentum().px())
        self.assertAlmostEqual(-3.140872e+00, particle.momentum().py())
        self.assertAlmostEqual(-9.044077e+00, particle.momentum().pz())
        self.assertEqual(11, particle.pid())

        # check 1st beam particle
        beam_particle_one: hm.GenParticle = vtx.particles_in()[0]
        self.assertAlmostEqual(0, beam_particle_one.momentum().px())
        self.assertAlmostEqual(0, beam_particle_one.momentum().py())
        self.assertAlmostEqual(-5, beam_particle_one.momentum().pz())
        self.assertEqual(11, beam_particle_one.pid())

        beam_particle_two: hm.GenParticle = vtx.particles_in()[1]
        self.assertAlmostEqual(0, beam_particle_two.momentum().px())
        self.assertAlmostEqual(0, beam_particle_two.momentum().py())
        self.assertAlmostEqual(110, beam_particle_two.momentum().pz())
        self.assertEqual(2212, beam_particle_two.pid())
        evt.clear()
        inputA.close()


    def test_convert_py6_eic(self):
        """Test detecting BeaGLE file type"""
        hepmc_convert(self._data_path('pythia6-radcor-10evt.txt'),
                      self._tmp_path('pythia6-radcor-10evt.hepmc'),
                      McFileTypes.UNKNOWN, "hepmc2")

        inputA = hm.ReaderAsciiHepMC2(self._tmp_path('pythia6-radcor-10evt.hepmc'))
        if inputA.failed():
            raise "inputA.failed()"

        evt = hm.GenEvent()
        inputA.read_event(evt)
        vtx: hm.GenVertex = evt.vertices()[0]
        particle: hm.GenParticle = vtx.particles_out()[0]

        self.assertAlmostEqual(-0.000341, particle.momentum().px())
        self.assertAlmostEqual(0.000687, particle.momentum().py())
        self.assertAlmostEqual(-9.711257, particle.momentum().pz())
        self.assertEqual(11, particle.pid())

        # check 1st beam particle
        beam_particle_one: hm.GenParticle = vtx.particles_in()[0]
        self.assertAlmostEqual(0, beam_particle_one.momentum().px())
        self.assertAlmostEqual(0, beam_particle_one.momentum().py())
        self.assertAlmostEqual(-10, beam_particle_one.momentum().pz())
        self.assertEqual(11, beam_particle_one.pid())

        beam_particle_two: hm.GenParticle = vtx.particles_in()[1]
        self.assertAlmostEqual(0, beam_particle_two.momentum().px())
        self.assertAlmostEqual(0, beam_particle_two.momentum().py())
        self.assertAlmostEqual(100, beam_particle_two.momentum().pz())
        self.assertEqual(2212, beam_particle_two.pid())
        evt.clear()
        inputA.close()
