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

Will try to autodetect the type and produce output.hepmc in HepMC3 format

Flags:

- -v, --verbose - Enable verbose output. Info level")
- -d, --debug - Enable debugging output. More than verbose")
- -i, --in-type - Input file type: [auto, pythia6-bnl, ...]
- -f, --format - HepMC format [2,3]
- -o, --output - "File name of resulting hepmc (default ouptut.hepmc)
- -s, --nskip - Number of events to skip
- -p, --nprocess - Number of events to process
- -b, --beam - adds beam particle. Must be "px,py,pz,e,pdg"


**Input formats:**

(for use with -i):

=============   ============  ==================================
format          -i arg        alternative
=============   ============  ==================================
Beagle          beagle
HepMC2          hepmc2
HepMC3          hepmc3
Pythia EIC      pythia_eic    pythia_bnl
Pythia6/LUND    lund          pythia_lund, lund_pythia, lund_py6
Lund GEMC       lund_gemc     pythia_gemc
EIC Smear       eic_smear
User defined       --         (ONLY trhough python API)
=============   ============  ==================================

If general mcconv can auto detect pythia6_EIC (or BNL).
The only thing it can't determine is original Pythia6 Lund and GEMC Lund
formats as they have exactly the same number of rows and columns.


**Beam particles**

Some MCEG don't store beam parameters or embed them in a file name. In such
cases users must provide beam info through `--beam` or `-b` flag. If you see
this error, it means that beam should be provided manually

.. code-block::

   For this type of text/lund file the beam information should be provided by user. But it was not provided


`--beam` should be called for each beam particle and is given in a form of a string
with coma separated values: "px, py, pz, e, pdg". See examples below.

**More examples**

.. code-block:: bash

    # Example 1. Minimal:
    mcconv input.txt -o output.hepmc

    # Example 2. Convert Lund GEMC with 10x110 beam (must be set manually for LUND):
    mcconv input.txt -i lund_gemc -b "0,0,-10,-10,11" -b "0,0,100,100,2212"

    # Example 3. Convert first 1000 events to HepMC2
    mcconv input.txt -p 1000 -f 2


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

Function `hepmc_convert` provides an interface to convert files similar to CLI.
(But much more flexible and extendable)

The minimal code:

.. code:: python

    from mcconv import hepmc_convert

    # This is minimal example.
    hepmc_convert('pythia6-radcor-10evt.txt', 'pythia6-radcor-10evt.hepmc')


In the above example PYTHIA6 EIC format can be automatically identified
and has all info needed for conversion (such as beam particles parameters).
The function will detect that it is PYTHIA6 EIC format, and convert all events in the file
 to HepMC3 (default)

Some old MCEG doesn't have information about the colliding beams and this info is mandatory

In this case an error like this will be shown:

.. code-block::

   For this type of text/lund file the beam information should be provided by user. But it was not provided


To solve this, one has to specify beam information manually.
Also sometimes it is impossible to distinguish between lund formats, as
the shape of files is completely the same, but column meanings are different.

The below example sets beam information manually
and points out that the input file is in LUND_GEMC format.
It is impossible to distinguish between LUND and LUND_GEMC formats - they look completely the same,
but LUND_GEMC pid and momentum columns are shifted compared to original LUND.

.. code:: python

    from mcconv import hepmc_convert

    # Beam particles in px, py, pz, e, pid
    beams = [
        (0, 0, -5., 5., 11),
        (0, 0, 110., 110., 2212),
    ]

    hepmc_convert('gemc-lund.3evt.txt', 'lund-convert.hepmc',
                  input_type = McFileTypes.LUND_GEMC,
                  beam_particles=beams)

Finally sometimes one needs to limit the number of events or save output to hepmc2 format
e.g. to use it with Delphes

.. code:: python

   from mcconv import hepmc_convert

   hepmc_convert('input.root', 'ouput.hepmc',       # input and output
                 input_type=McFileTypes.EIC_SMEAR,  # File type
                 hepmc_vers=2,                      # HepMC version 2 or 3
                 nskip=10                           # Skip 10 events *
                 nprocess=1000)                     # number of events to process

..

 *nskip* - for text formats it is impossible to skip events without consequently parsing
 a file. In this case nskip takes almost the same amount of time as processing events.
 Binary formats, such as root in the above example can skip X events fast


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

If `McFileTypes.UNKNOWN` is provided, hepmc_convert tries to **autodetect** type.
One can also do it by autodetect function:

.. code:: python

    from mcconv import detect_mc_type

    mc_file_type = detect_mc_type('my_file.root')

If `McFileTypes.USER` is provided, some extended parameters are required such as
custom conversion rules, or customized reader, etc. The next chapter explains this.


Convert any lund-like format
----------------------------

Lets look how in general text formats look to understand how to
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
- All lines that have "==" are irrelevant
- Event and particle lines have different number of columns
- Particles are lines that follow Event line until the next Event or end of file

In order to parse the most of such file types mcconv has `GenericTextReader` class.
To do the job it has the next approach while parsing file line by line:

- determine if line is relevant. If yes - tokenize it
- determine tokens are an event or particle
- build events consisting of unparsed tokens

In general users can set their own function which do this determination and implement pretty
complex logic of event building (explained in Advanced topics section)

By default `GenericTextReader` is set up so that it can read many of the BNL and JLab defined
files with a minimum setup.

The default settings are:

- Skip all lines that have any letters or "==" or are empty
- Determine is it event/particle line by the number of columns

So in many cases one just can setup the number of columns (or tokens) in the particle line. 10 for
the next example. `hepmc_convert` function may accept user configured reader.

.. code-block:: python

    reader = GenericTextReader()
    reader.particle_tokens_len = 10   # particles has 10 columns, events have another number of columns
    hepmc_convert('input.root', 'ouput.hepmc', reader=reader, ...)

This example is not yet complete as one also has to set what columns correspond to PID, momentums, etc.
In many cases it is just the same as for the common Pythia6 or LUND formats, so
one can use existing definition

.. code-block:: python

   from mcconv import hepmc_convert, GenericTextReader, McFileTypes

   reader = GenericTextReader()
   reader.particle_tokens_len = 14   # particles has 14 columns, events have another number of columns
   # The columns order is the same as in LUND
   hepmc_convert('input.root', 'ouput.hepmc', reader=reader, input_type=McFileTypes.LUND)

Or one has to provide conversion rules. The rules are pretty self explanatory... to some level:

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
                  input_type=McFileTypes.USER,     # <= (!) note it must be USER
                  rules=rules)                     # <= it must be not None


Conversion rules explained
^^^^^^^^^^^^^^^^^^^^^^^^^^

While rules are self explanatory, there are things that needs explanation.

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
          # imagine MCEG that writes colliding beams as the first 2 particles
          if particle_line_index in [0,1]:
              return 4      # 4 - beam particle status in HepMC

          # status_token here is not yet parsed
          generator_status = int(status_token)

          # return 1 for stable particles and 0 otherwise
          if generator_status == 1:
              return 1      # 1 - stable particle
          else:
              return 0      # 0 - will be thrown away in case of flat conversion

    # set rules, how we convert status:
    rules["status"] = (1, convert_status)  # status column index + conversion function

**beam_rule** must be defined

HepMC Event has to have at least one vertex that must have at least one input particle.
For EIC MCEG in case of flat conversion (no full topology) we await that there will be one vertex
with two incoming beam particles. It make sense, as even if
one has an old generator that doesn't store such information, one has to know beam parameters
to run the simulation. The problem here is that old generators do different tricks to store
beam data. Such as:

1. Store beam info in event header
2. Provide beam particles as a first 2 particles in event
3. Use status (usually not corresponding to HepMC beam particle status = 4)
4. Use special flag or special status
5. Embed beam params in file name
6. etc. etc. etc.

Currently mcconv knows several ways to automatically extract beam parameters.
They are defined by `beam_rule`.

beam_rule are:

.. code-block:: python

    # manual - users define beam particles through flags, arguments, etc.
    "beam_rule": "manual"

    # status - look at status code. status=4 - beam particle. Must be present in every event
    # Usually works good with status conversion function (see above)
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
                  rules=rules,
                  beam_particles=beams)            # beam particles since "beam_rule": "manual"


Boost, rotate, shift and count events
-------------------------------------

Users can register callbacks that allow to modify hepmc events before they are saved, report number
of events, etc. It allows to apply boost, rotate, shift for hepmc event (mcconv doesn't have
afterburner with beam effects... yet).

User can set the next callback functions to hepmc_convert:

- `begin_func(writer, reader, input_type)` is called before events are being read.
   Can be used to store run info, check parameters, change input_type, etc.
- `transform_func(evt_index, hepmc_event)` - is called when hepmc_event is formed but not
   yet written. Can be used to change hepmc event before saving (boost, rotate, etc).
- `progress_func(evt_index, hepmc_event)` - is called after each event is saved.
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
                      begin_func=on_start_processing,            # Add callbacks
                      transform_func=boost_rotate,
                      progress_func=show_progress,
                      nprocess=3
                      )

Advanced topics
---------------

Generic GenericReader
^^^^^^^^^^^^^^^^^^^^^

As one could guess in case the number of columns for events and particles are the same,
setting just `reader.particle_tokens_len = 12` is not enough and some more complex rules needed
(for example looking for "===event start===" kind of lines). In this case one can provide
functions with extended logic:

- `is_line_relevant`,
- `is_event`
- `is_particle`.

.. code-block:: python

    # example for a file where both event and particle has 14 columns
    # but each event prepended with "==event start==" line

    HAS_LETTERS_RE = re.compile('[a-df-zA-DF-Z]')  # skip e for exponent
    is_prev_line_event = False                     # previous line was "==event start=="


    def my_is_line_relevant(self, line):
        """ check if the line is comment or somthing """
        if "==event start==" in line:     # it is "==event start==" but it its irrelevant by itself
            is_prev_line_event = True
            return False

        if "=" in line or "#" in line:
            return False

        has_letters = HAS_LETTERS_RE.search(line)
        has_letters = bool(has_letters)
        return not has_letters

    def my_is_event(self, tokens):
        """ check it is event """
        if is_prev_line_event:
            is_prev_line_event = False
            if len(tokens) == 14          # Previous line was "==event start==" and here 14 values
                return True
        return False

    def my_is_particle(self, tokens):
        """ check it is particle info """
        return len(tokens) == 14 and not is_prev_line_event

    reader = GenericReader(is_line_relevant=my_is_line_relevant,
                           is_event=my_is_event,
                           is_particle=my_is_particle)


Another way is to inherit from GenericTextReader and make it even more complex. Do you need it?

Any class that has reader functions will work as a GenericTextReader replacement if it
returns `TextFileEvent` with the next interface

.. code-block:: python

  TextFileEvent:
      started_at_line;    // Line number at which the event has started
      event_tokens;       // Tokens like ["0", "1", "1", "11", "2", "1", ...] from 'event' related line/s
      record_tokens       // Tokens like ["1", "21", "22122", ...] from each particle or 'record' lines


Custom readers
^^^^^^^^^^^^^^

Users can provide completely custom readers, e.g. that could read custom root files, etc.

Any reader should follow a simple interface:

.. code-block:: python

   class MyReader:

      def open(file_name):
         # opens a file with file_name

      def events(self, nskip: int = 0, ntake: int = 0):
         # should return a generator that yields some objects with Event information

      def close():
         # closes the file.
         # Readers don't follow 'with', __enter__() and __exit__() as pyHepMC don't follow them


What is that "some objects with Event information"? Actually it could be anything. With any
custom reader you have to provide "conversion" function that knows how to convert
such event to hepmc event. As it is said above `GenericTextReader` returns `TextFileEvent` objects
and you can find `lund_to_hepmc` function in mcconv that knows how to convert `TextFileEvent`-s.

The signature of a conversion function is:

.. code-block:: python

    def my_convert_func(evt_index, hepmc_event, source_event, rules=rules, beam_particles=beam_particles):
    """
        Converts from custom events to hepmc_event

        @evt_index - it is IO event index, like index in file
        @hepmc_event - output hepmc event object
        @source_event - input object with event data
        @rules - anything that helps defining conversion rules (usually map with configs)
        @beam_particles - a list of tuples [(px, py, pz, e, pid)] if provided by user
    """

With having both you can provide the reader and the converter to hepmc_convert

.. code-block:: python

    hepmc_convert( # ...
                   reader = MyReader(),
                   convert_func = my_convert_func)

    # one more example how you can pass your own custom rules
    hepmc_convert( # ...
                   reader = MyReader(),
                   convert_func = my_convert_func,
                   rules = {"my_rule_number_one": "no-rules"})  # just example how you can pass custom rules
Please see mcconv/eic_smear_reader.py and eic_smear_to_hepmc(...) function as an example of root file
conversion