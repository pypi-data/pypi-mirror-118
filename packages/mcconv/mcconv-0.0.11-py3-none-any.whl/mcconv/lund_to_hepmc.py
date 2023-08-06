import copy
from pyHepMC3 import HepMC3 as hm
from mcconv import McFileTypes, UnparsedTextEvent


def add_hepmc_attribute(obj, name, str_value, val_type):
    if val_type == int:
        obj.add_attribute(name, hm.IntAttribute(int(str_value)))
    if val_type == float:
        obj.add_attribute(name, hm.FloatAttribute(float(str_value)))
    if val_type == str:
        obj.add_attribute(name, hm.StringAttribute(str_value))


LUND_RULES = {
    "px": 6,        # Column where px is stored
    "py": 7,        # Column where py is stored
    "pz": 8,        # Column where pz is stored
    "e": 9,         # Energy
    "pid": 2,       # PID of particle (PDG code)
    "status": 1,    # Status
    "evt_attrs": {"weight": (9, float)},        # That is how one can store event level data
    "prt_attrs": {},
    "beam_rule": "manual"
}

LUND_GEMC_RULES = {
    "px": 6,        # Column where px is stored
    "py": 7,        # Column where py is stored
    "pz": 8,        # Column where pz is stored
    "e": 9,         # Energy
    "pid": 3,       # PID of particle (PDG code)
    "status": 2,    # Status
    "evt_attrs": {"weight": (9, float)},        # That is how one can store event level data
    "prt_attrs": {"life_time": (1, float)},     # In LUND GemC the second col. (index 1) is life time.
    # If that is need to be stored, that is how to store it
    "beam_rule": "manual"
}

BEAGLE_RULES = copy.deepcopy(LUND_RULES)
BEAGLE_RULES["beam_rule"] = "beagle"
BEAGLE_RULES["evt_attrs"] = {"weight": (-5, float), # 5th from the right... hehe
                             "atarg": (4, float),
                             "ztarg": (5, float)}



PYTHIA6_EIC_RULES = copy.deepcopy(LUND_RULES)
PYTHIA6_EIC_RULES["beam_rule"] = "first_lines"

# A map of rules by HepMC
LUND_CONV_RULES = {
    McFileTypes.BEAGLE: BEAGLE_RULES,
    McFileTypes.LUND: LUND_RULES,
    McFileTypes.LUND_GEMC: LUND_GEMC_RULES,
    McFileTypes.PYTHIA6_EIC: PYTHIA6_EIC_RULES
}


def lund_to_hepmc(hepmc_evt, unparsed_event, rules, beam_particles=None):
    """
        Rules define columns, that are used for extraction of parameters

        rules = {
            "px": 6,        # Column where px is stored
            "py": 7,        # Column where py is stored
            "pz": 8,        # Column where pz is stored
            "e": 9,         # Energy
            "pid": 2,       # PID of particle (PDG code)
            "status": 1,    # Status
            "evt_attrs": {"weight": (9, float)},        # That is how one can store event level data
            "prt_attrs": {"life_time": (1, float)},     # In LUND GemC the second col. (index 1) is life time.
                                                        # If that is need to be stored, that is how to store it
            "beam_rule":  "manual"            # users must provide beam parameters through flags/arguments
        }
        rules["px"]
        rules["py"]
        rules["pz"]
        rules["e"]
        rules["pid"]
        rules["status"]
        rules["evt_attrs"]
        rules["prt_attrs"]

    """
    assert isinstance(unparsed_event, UnparsedTextEvent)

    prt_col_px = rules["px"]
    prt_col_py = rules["py"]
    prt_col_pz = rules["pz"]
    prt_col_e = rules["e"]
    prt_col_pid = rules["pid"]
    prt_col_status = rules["status"]
    evt_attrs = rules["evt_attrs"]
    prt_attrs = rules["prt_attrs"]
    prt_beam_rule = rules["beam_rule"]

    hepmc_evt.add_attribute("start_line_index", hm.IntAttribute(unparsed_event.start_line_index))

    v1 = hm.GenVertex()
    
    # do we have a manual beam particles? 
    
    if prt_beam_rule == "manual":

        # sanity check
        if not beam_particles:
            raise ValueError("For this type of text/lund file the beam information should be provided by user. "
                             "But it was not provided")

        # add user provided beam particles
        for beam_particle in beam_particles:
            px, py, pz, energy, pid = tuple(beam_particle)
            hm_beam_particle = hm.GenParticle(hm.FourVector(px, py, pz, energy), pid, 4)
            v1.add_particle_in(hm_beam_particle)
            hepmc_evt.add_particle(hm_beam_particle)

    # particles = parse_lund_particles(unparsed_event)
    for particle_index, particle_line in enumerate(unparsed_event.unparsed_particles):

        # Parse main columns with 4 vectors
        px = float(particle_line[prt_col_px])
        py = float(particle_line[prt_col_py])
        pz = float(particle_line[prt_col_pz])
        energy = float(particle_line[prt_col_e])
        pid = int(particle_line[prt_col_pid])
        if isinstance(prt_col_status, (list, tuple)):
            # is it a tuple like
            status = prt_col_status[1](particle_index, particle_line[prt_col_status[0]])
        else:
            status = int(particle_line[prt_col_status])

        # Set beam particle status as 4 for the first 2 particles
        if prt_beam_rule == "first_lines" and particle_index in [0, 1]:
            status = 4

        # Take only final state particle
        if status not in [1, 4]:
            continue

        # Create a hepmc particle
        hm_beam_particle = hm.GenParticle(hm.FourVector(px, py, pz, energy), pid, status)

        hepmc_evt.add_particle(hm_beam_particle)

        # Add particle level attributes
        for name, params in prt_attrs.items():
            column_index, field_type = params
            add_hepmc_attribute(hm_beam_particle, name, particle_line[column_index], field_type)

        # Add particle to event
        if status == 4:
            # Beam particle
            v1.add_particle_in(hm_beam_particle)
        else:
            # All other particles
            v1.add_particle_out(hm_beam_particle)



        # Add event level attributes
        for name, params in evt_attrs.items():
            column_index, field_type = params
            add_hepmc_attribute(hepmc_evt, name, unparsed_event.event_tokens[column_index], field_type)

    hepmc_evt.add_vertex(v1)
    return hepmc_evt