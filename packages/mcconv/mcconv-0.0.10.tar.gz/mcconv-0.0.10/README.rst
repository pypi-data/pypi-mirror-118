mcconv
======

**(!) The library is under development.
Many of the features will be implemented on the first request!
`Request features here <https://eicweb.phy.anl.gov/monte_carlo/mcconv/-/issues>`_ (!)**

Converter of MCEG  files from old EIC generators to HEPMC.

Provides command line interface (CLI) and python API to convert old (and not old) event
generators mainly used for EIC to HepMC.

**CLI supported types** (out of the box):

- LUND (vanilla pythia6)
- LUND GEMC (various generators especially from Clas12)
- Pythia6 RadCor (aka Pythia-EIC, Pythia6-BNL, Pythia6-HERMES)
- Beagle
- Eic-smear (aka Eic-tree)

**Python API supported types**

- Any type of text event+particles formats
- Eic-smear (aka Eic-tree)



mcconv command line
~~~~~~~~~~~~~~~~~~~


.. code:: bash

    pip install mcconv
    mcconv my_file.txt

Will try to autodetect the type and produce my_file.hepmc

Flags:

- -d, --debug - Enable debugging output. More than verbose")
- -v, --verbose - Enable verbose output. Info level")
- -i, --in-type - Input file type: [auto, pythia6-bnl, ...]
- -f, --format - HepMC format [2,3]
- -o, --output - "File name of resulting hepmc (default ouptut.hepmc)
- -s, --nskip - Number of events to skip
- -p, --nprocess - Number of events to process

Input formats (for use with -i):

=============   ============  ==================================
format          -i arg        alternative
=============   ============  ==================================
Beagle          beagle
HepMC2          hepmc2
HepMC3          hepmc3
Pythia EIC      pythia_eic    pythia_bnl
Pythia6_lund    lund          pythia_lund, lund_pythia, lund_py6
lund_gemc       lund_gemc     pythia_gemc
EIC Smear       eic_smear
User defined       --         (ONLY trhough python API)
=============   ============  ==================================

If general mcconv can auto detect pythia6_EIC (or BNL).
The only thing it can't determine is original Pythia6 Lund and GEMC Lund
formats as they have exactly the same number of rows and columns.


Flat vs topologic convert
-------------------------

There are two conversion methods: **flat** and **topologic** convert.

HepMC assumes event as a graph of vertexes and particles.


**topologic** conversion (IS NOT IMPLEMENTED and will be implemented on the first
requiest or in some future) - tries to convert all particles and build hepmc graph.

.. code::
                          p7
    p1                   /
      \v1__p3      p5---v4
            \_v3_/       \
            /    \        p8
       v2__p4     \
      /            p6
    p2



**flat** conversion just uses final state particle 4 vectors and put them
into a single hepmc vertex. One can add particle and event level attributes
(like true x and Q2, polarization, etc).

This method is the fastest and the only needed method for a further processing
with DD4Hep or Delphes.

.. code::

    beam_a     |- p1
         \     |- p2
          \_v1_|- p3
          /    |- ...
         /     |- pn
    beam_b



Python API
~~~~~~~~~~

Python API allows to:

1. Convert MC files (same as CLI)
3. Read MC files event by event (partially implemented)
2. Read MC files as Pandas arrays (in implementation)
4. Read MC files as Awkward arrays (planned)


Convert to HepMC
----------------

.. code:: python

   from mcconv import hepmc_convert

   hepmc_convert('input.root', 'ouput.hepmc',
                 input_type=McFileTypes.EIC_SMEAR,
                 hepmc_vers=3,
                 nprocess=100000)


Where McFileTypes is one of:

.. code:: python

    McFileTypes.UNKNOWN
    McFileTypes.USER
    McFileTypes.BEAGLE
    McFileTypes.HEPMC2
    McFileTypes.HEPMC3
    McFileTypes.LUND
    McFileTypes.LUND_GEMC
    McFileTypes.PYTHIA6_EIC
    McFileTypes.EIC_SMEAR

If McFileTypes.UNKNOWN is provided, hepmc_convert tries to **autodetect** type.
One can also do it by autodetect function:

.. code:: python

    from mcconv import detect_mc_type

    mc_file_type = detect_mc_type('my_file.root')


Convert any lund like format
----------------------------

Lets look how in general lund formats look, to understand how to
setup mcconv to convert them

.. code-block::

   PYTHIA EVENT FILE
   ============================================
   I, ievent, genevent, subprocess, (40 event columns descriptions)
   ============================================
   I  K(I,1)  K(I,2)  K(I,3)  K(I,4) (10 particle columns description)
   ============================================
     0          1    1   95 2212         ... (other event columns)
   ============================================
       1     21         11        0      ... other particle columns
       2     21       2212        0      first 2 particles are beam
       3     21         11        1      ...
       4     21         22        1      ...
       5     21       2212        2      ...
          ... many other particles ...
      26      1        211       18      ...
      27     11        111       18      ...
      28      1         22       23      ...
      29      1         22       23      ...
      30      1         22       27      ...
      31      1         22       27      ...
   =============== Event finished =======...

So in terms of parsing such events we may notice:

- First 6 lines are irrelevant
- All lines that have "==" in them are irrelevant
- Event and particle lines have different number of columns
- Particles are relevant lines that follow Event line until the next Event or end of file

In order to parse the most of such file types mcconv has `class GenericTextReader`. To do the job
it has the next approach going file line by line:

- determine if line is relevant. If yes - tokenize it
- determine the line an event or particle
- combine events base

In general users can set their own function which do this determination and implement pretty
complex logic of event building. But this is an advanced example.

By default `GenericTextReader` is set up so that it can read the most of the BNL and JLab defined
files with a minimum setup.

The default settings are:

- Skip all lines that have any letters or "==" or consist of empty characters
- Determine is it event/particle line by the number of columns

So in many cases one just can setup the number of columns (or tokens) in the particle line. 10 for
the current one. `hepmc_convert` function may accept user configured reader.

.. code-block:: python

    reader = GenericTextReader()
    self.particle_tokens_len = 10   # particles has 10 columns
    hepmc_convert('input.root', 'ouput.hepmc', reader=reader, ...)

This example is not yet complete as one also has to set what columns correspond to PID, momentums, etc.
In many times it is just the same as for the common Pythia6 formats (with some columns added). So
one can use existing definition

.. code-block:: python

   from mcconv import hepmc_convert

   reader = GenericTextReader()
   self.particle_tokens_len = 10   # particles has 10 columns
   hepmc_convert('input.root', 'ouput.hepmc', reader=reader, input_type=McFileTypes.EIC_SMEAR)

Or one has to provide conversion rules. The rules are pretty self explanatory to some degree:

.. code-block:: python

    from mcconv import GenericTextReader, hepmc_convert, McFileTypes
    # define how particle and event information is stored (indexes are 0 based)
    rules = {
       "px": 6,        # Column index where px is stored
       "py": 7,        # Column index where py is stored
       "pz": 8,        # Column index where pz is stored
       "e": 9,         # Column index Energy
       "pid": 2,       # Column index PID of particle (PDG code)
       "status": 1,    # Column index Status
       "evt_attrs": {"weight": (9, float)},        # That is how one can store event level data columns
       "prt_attrs": {"life_time": (1, float)},     # In LUND GemC the second col. (index 1) is life time.
                                                   # If that is need to be stored, that is how to store it
       "beam_rule": "manual"                       # users must provide beam parameters through flags/arguments
    }

    reader = GenericTextReader()
    reader.particle_tokens_len = 10   # particles has 10 columns
    hepmc_convert('input.root', 'ouput.hepmc',
                  reader=reader,
                  input_type=McFileTypes.USER,     # <= note it must be USER
                  text_conv_rules=rules)           # <= it must be not None


Conversion rules details
^^^^^^^^^^^^^^^^^^^^^^^^

While rules are self explanatory, there are things that needs explanation:

**Status in generators may not correspond to HepMC status**. HepMC statuses:

=============   ======================================================
status          description
=============   ======================================================
0               Not defined (null entry) Not a meaningful status
1               Undecayed physical particle Recommended for all cases
2               Decayed physical particle Recommended for all cases
3               Often used for in/out particles in hard process
4               Incoming beam particle Recommended for all cases
5–10            Reserved for future standards Should not be used
11–200          Generator-dependent For generator usage
201–            Simulation-dependent For simulation software usage
=============   ======================================================

In order to mitigate it, users may pass a function that convert a
status from a generator to HepMC status:

.. code-block:: python

    # Imagine pythia EIC case where the first 2 particles are beam particles
    def convert_status(particle_line_index, status_token, all_prt_tokens):
          # first 2 particles are beam particles
          if particle_line_index in [0,1]:
              return 4

          # status_token here is not yet parsed
          generator_status = int(status_token)

          # return 1 for stable particles and 0 otherwise
          if generator_status == 1:
              return 1
          else:
              return 0


    rules["status"] = (1, convert_status)  # status column index + conversion function

**beam_rule** must be defined

HepMC Event has to have at least one vertex that should have at least one input particle.
For EIC MCEG with flat conversion (no full topology) we await that there will be one vertex
with two incoming particles corresponding to beam particles. It make sense as even if
one has an old generator that doesn't store such information, one has to know corresponding beam
information for the simulation. The problem here, that old generators do different tricks to store
such data. Such as:

1. Store beam info in event header
2. Provide beam particles as a first 2 particles in event
3. Use status (usually not corresponding to HepMC beam particle status = 4)
4. Use special flag or special status
5. Embed beam params in file name
6. etc. etc. etc.

Currently mcconv knows several ways to extract beam parameters. They are defined by `beam_rule`

beam_rule are:

.. code-block:: python

    # manual - users define beam particles through flags, arguments, etc.
    "beam_rule": "manual"

    # status - look at status code. 4 = beam particle. Must be present in every event
    # works good with status conversion function (see above)
    "beam_rule": "status"

    # first 2 particles are beam particles
    "beam_rule": "first_lines"

    # BeAGLE specific
    "beam_rule": "beagle"

    # more use cases needed for more rules!


Here is the full example which you can find in `examples/custom_lund_format.py`

.. code-block:: python

    from mcconv import GenericTextReader, hepmc_convert, McFileTypes

    # define how particle and event information is stored (indexes are 0 based)
    rules = {
        "px": 6,        # Column where px is stored
        "py": 7,        # Column where py is stored
        "pz": 8,        # Column where pz is stored
        "e": 9,         # Energy
        "pid": 2,       # PID of particle (PDG code)
        "status": 1,    # Status
        "evt_attrs": {"weight": (9, float)},        # That is how one can store event level data
        "prt_attrs": {},
        "beam_rule": "manual"                       # provide beam particles manually
    }

    # Beam particles in px, py, pz, e, pid
    beams = [(0, 0, -5., 5., 11),
             (0, 0, 110., 110., 2212)]

    # Setup file event reader
    reader = GenericTextReader()
    reader.particle_tokens_len = 12   # particles has 10 columns

    # Run conversion
    hepmc_convert('custom_lund_format.txt', 'custom_lund_format.hepmc',
                  reader=reader,
                  input_type=McFileTypes.USER,     # <= note it must be USER
                  text_conv_rules=rules,
                  beam_particles=beams)            # beam particles since "beam_rule": "manual"



Boost, rotate, shift and count events
-------------------------------------

Users can register callbacks that allow to modify hepmc events before and after event is saved
The first allows e.g. to apply hepmc boost, rotate, shift for hepmc event (mcconv doesn't have
afterburner with beam effects... yet).

User can provide 3 functions to hepmc_convert:

 - `init_func(writer, reader, input_type)` is called before events are being read.
   Can be used to sture run info, check reader parameters, input_type, etc.
 - `transform_func(evt_index, hepmc_event)` - is called when hepmc_event is formed but not
   yet written. Can be used to change hepmc event before saving.
 - `progress_func(evt_index, hepmc_event)` - is called when event processing is over.
   Can be used to print progress.


You can test it in `examples/callbacks_and_boost_rotate.py` example file:

.. code-block:: python

    import sys
    from mcconv import hepmc_convert, McFileTypes
    from pyHepMC3 import HepMC3 as hm


    def on_start_processing(writer, reader, input_type):
        print("Ready to start processing")
        print(f"  writer:     {writer}")
        print(f"  reader:     {reader}")
        print(f"  input_type: {input_type}")


    def show_progress(event_index, evt):
        """Shows event progress"""
        print(f"Events processed: {event_index:<10}")
        # we could print evt here too
        # hm.Print.content(evt)
        # hm.Print.listing(evt)


    def boost_rotate(event_index, evt):
        boost_vector = hm.FourVector(0, 0.002, 0.0, 0.001)
        #  Test that boost with v=0 will be OK
        assert True == evt.boost(boost_vector)
        rz = hm.FourVector(0.0, 0.0, -0.9, 0)
        rzinv = hm.FourVector(0.0, 0.0, 0.9, 0)
        evt.rotate(rz)
        evt.rotate(rzinv)


    if __file__ == "__main__":

        hepmc_convert('../test/data/pythia6-radcor-10evt.txt',   # input
                      'cpythia6-radcor-10evt.hepmc',             # output
                      input_type=McFileTypes.UNKNOWN,            # Autodetect file type
                      init_func=on_start_processing,             # Add callbacks
                      transform_func=boost_rotate,
                      progress_func=show_progress,
                      nprocess=3
                      )
