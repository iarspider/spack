# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import shutil
import os

class Openloops(Package):
    """The OpenLoops 2 program is a fully automated implementation of the
       Open Loops algorithm combined with on-the-fly reduction methods,
       which allows for the fast and stable numerical evaluation of tree
       and one-loop matrix elements for any Standard Model process
       at NLO QCD and NLO EW. """

    homepage = "https://openloops.hepforge.org/"
    url      = "https://openloops.hepforge.org/downloads?f=OpenLoops-2.1.1.tar.gz"

    version('2.1.1', sha256='f1c47ece812227eab584e2c695fef74423d2f212873f762b8658f728685bcb91')

    all_processes = (
        "tbln", "tbln_ew", "tbqq", "tbw", "pptttt", "pptttt_ew", "pptt",
        "pptt_ew", "ppttbb", "ppttj", "ppttj_ew", "ppttjj",
        "pptaj", "pptajj", "pptllj", "pptlljj", "pptln", "pptw", "pptwj",
        "pptzj", "pptzjj", "ppthj", "ppthjj", "pptj",
        "pptjj", "ppjj", "ppjj_ew", "ppjjj", "ppjjj_ew", "ppjjj_nf5", "ppjjjj",
        "pplllvvv_ew", "ppatt", "ppatt_ew",
        "ppattj", "pplltt", "pplltt_ew", "ppllttj", "ppllttj_ew", "pplntt",
        "pplnttj", "ppwtt", "ppwtt_ew", "ppwttj",
        "ppwttj_ew", "ppztt", "ppztt_ew", "ppzttj", "ppaatt", "ppwwtt",
        "ppzatt", "ppzztt", "ppvvvv", "ppaaaj2", "ppllaa",
        "ppllaaj", "pplllla", "ppvvv", "ppvvv2", "ppvvv_ew", "ppvvvj", "ppaajj",
        "ppaajj2", "ppaajjj", "pplla", "pplla2",
        "pplla_ew", "ppllaj", "ppllaj2", "ppllaj_ew", "ppllaj_nf5", "ppllajj",
        "ppllll", "ppllll2", "ppllll2_nf5",
        "ppllll2_onlyh", "ppllll_ew", "ppllllj", "ppllllj2", "ppllllj2_nf5",
        "ppllllj2_nf5_notridr", "ppllllj2_nf5_sr",
        "ppllllj2_onlyh", "ppllnnjj_ew", "ppllnnjj_vbs", "pplnajj", "ppvv",
        "ppvv2", "ppvv_ew", "ppvvj", "ppvvj2",
        "ppvvj_ew", "ppwajj", "ppwwjj", "ppzajj", "ppzwj_ew", "ppzwjj",
        "ppzzjj", "ppajj", "ppajj2", "ppajj_ew", "ppajjj",
        "ppllj", "ppllj2", "ppllj_ew", "ppllj_nf5", "pplljj", "pplljj_ew",
        "pplljjj", "pplnj_ckm", "pplnjj", "pplnjj_ckm",
        "pplnjj_ew", "pplnjjj", "ppnnjj_ew", "ppnnjjj", "ppvj", "ppvj2",
        "ppvj_ew", "ppwj_ckm", "ppwjj", "ppwjj_ckm",
        "ppwjj_ew", "ppwjjj", "ppzjj", "ppzjj_ew", "ppzjjj", "pphtt",
        "pphtt_ew", "pphttj", "pphlltt", "pphll", "pphll2",
        "pphll_ew", "pphllj", "pphllj2", "pphllj_ew", "pphlljj", "pphlljj_top",
        "pphlnj_ckm", "pphlnjj", "pphv", "pphv_ew",
        "pphwjj", "pphz2", "pphzj2", "pphzjj", "pphhtt", "pphhv", "pphhh2",
        "heftpphh", "heftpphhj", "heftpphhjj", "pphh2",
        "pphhj2", "pphhjj2", "pphhjj_vbf", "bbhj", "heftpphj", "heftpphjj",
        "heftpphjjj", "pphbb", "pphbbj", "pphj2",
        "pphjj2", "pphjj_vbf", "pphjj_vbf_ew", "pphjjj2", "eetttt", "eettttj",
        "eellllbb", "eett", "eett_ew", "eettj",
        "eettjj", "eevtt", "eevttj", "eevttjj", "eevvtt", "eevvttj",
        "eellll_ew", "eevv_ew", "eevvjj", "eell_ew", "eevjj",
        "eehtt", "eehttj", "eehll_ew", "eehvtt", "eehhtt", "heftppllj",
        "heftpplljj", "heftpplljjj")

    variant('compile_extra', default=False, 
            description='Compile real radiation tree amplitudes')
    variant('processes', description='Processes to install. See https://'+
                                     'openloops.hepforge.org/process_'+
                                     'library.php?repo=public for details',
            values=disjoint_sets(('all.coll',), ('lhc.coll',), ('lcg.coll',), 
                                 all_processes).with_default('lhc.coll'))

    variant('num_jobs', description='Number of parallel jobs to run. ' +
                                    'Set to 1 if compiling a large number' +
                                    'of processes', default=0)
    depends_on('python', type=("build", "run"))

    phases = ['configure', 'build', 'build_processes', 'install']

#    def setup_build_environment(self, env):
#      env.set("CC", self.compiler.cc)
#      env.set("CXX", self.compiler.cxx)
#      env.set("FC", self.compiler.fc)
#      env.set("F77", self.compiler.fc)
#      env.set("FORTRAN", self.compiler.fc)
#      env.set("PATH", "/bin:/usr/bin:")

    def configure(self, spec, prefix):
        with open('openloops.cfg', 'w') as f:
            print('[OpenLoops]', file=f)
            print('num_jobs = {0}'.format(self.spec.variants['num_jobs'].value), file=f)
            print('cc = {0}'.format(self.compiler.cc), file=f)
            print('cxx = {0}'.format(self.compiler.cxx), file=f)
            print('fortran_compiler = {0}'.format(self.compiler.fc), file=f)
            if self.spec.satisfies('@1.3.1') and not self.spec.satisfies('%intel'):
                print('gfortran_f_flags = -ffree-line-length-none')
            if self.spec.satisfies('@2.1.1') and not self.spec.satisfies('%intel'):
                print('gfortran_f_flags = -ffree-line-length-none -fdollar-ok -mcmodel=medium')

        if self.spec.satisfies('@:1.999.999'):
            copy(join_path(os.path.dirname(__file__), 'sft1.coll'), 'lcg.coll')
        elif self.spec.satisfies('@2:2.999.999'):
            copy(join_path(os.path.dirname(__file__), 'sft2.coll'), 'lcg.coll')

    def build(self, spec, prefix):
        scons = Executable('./scons')
        scons('generator=1', 'compile=2')

    def build_processes(self, spec, prefix):
        ol = Executable('./openloops')
        processes = self.spec.variants['processes'].value
        if not isinstance(processes, str):
            processes = [processes]
        if self.spec.variants['compile_extra']:
            ce = 'compile_extra=1'
        else:
            ce = ''

        ol('libinstall', ce, *processes)

    def install(self, spec, prefix):
#        shutil.rmtree('process_obj')
#        shutil.rmtree('process_src')

        install_tree(self.stage, self.prefix, ignore=lambda x: x in ('process_obj', 'process_src'))
#        for p in os.listdir(self.stage):
#            if os.path.isdir(p):
#                copy_tree(p)
#            else:
#                install(p)
	# TODO
