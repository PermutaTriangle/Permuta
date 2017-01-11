## Functions to move from `permutation.py` to the `Perm` class(to start with):
[X] monotone_increasing
[X] monotone_decreasing
[X] identity
[X] random
[ ] random_avoider : will probably be moved to PermSet.py
[ ] listall : will probably be moved to PermSet.py or removed
[X] standardize
[ ] change_repr : needs discussion
[X] ind2perm : called `unrank`
[X] swap : subroutine of ind2perm
[ ] plentiful : TODO understand wtf this does
[X] segment : subroutine of plentiful
[X] _is_iterable : not needed
[X] __call__
[X] oneline : standard representation of the permutations as a tuple
[X] cycles : copied as `cycle_notation`
[X] \__repr__
[X] \__mul__
[X] \__add__
[X] \__sub__
[X] \__pow__
[ ] perm2ind : TODO implement as `rank`
[X] delete : implemented as `remove`
[X] insert
[X] complement
[X] reverse
[X] inverse
[X] _ascii_plot
[X] cycle_decomp
[X] direct_sum
[X] skew_sum
[X] fixed_points
[X] skew_decomposable : copied as `is_skew_decomposable` RAGGI
[X] sum_decomposable : copied as `is_sum_decomposable` RAGGI
[X] num_cycles : copied as `count_cycles`
[X] descent_set
[X] num_descents : copied as `count_descents`
[X] ascent_set
[X] num_ascents : copied as `count_ascents`
[X] peak_list
[ ] check
[X] num_peaks : copied as count_peaks
[X] valley_list
[X] num_valleys : copied as `conut_valleys`
[ ] bend_list : not implemented in `permpy` anyways
[ ] trivial : this is stupid
[X] order
[X] ltrmin
[X] rtlmin
[X] ltrmax
[X] rtlmax
[X] num_ltrmin
[X] inversions : should be reimplemnted in N*logN as `count_inversions`
[X] min_gapsize
[X] noninversions : should be reimplemented as count_noninversions using inversions
[X] bonds : should be copied as count_bonds
[X] majorindex
[ ] fixedptsplusbonds : returns sum of fixed points and bonds, not needed?
[X] longestrunA : maybe change name? maybe return indices instead of length? copied as `longestrun_ascending`
[X] longestrunD : maybe change name? maybe return indeces instead of length? copied as `longestrun_descending`
[X] longestrun : maybe return indices instead of length, then add `count_longestrun`
[ ] christiecycles : WTF
[ ] othercycles : WTF
[ ] sumcycles : WTF
[ ] maxcycles : WTF
[X] is_involution
[X] is_identity
[ ] threepats
[ ] fourpats
[ ] num_consecutive_3214 : makes no freakin sense to have here
[ ] coveredby : looks unneaded and weird
[ ] buildupset : looks weird
[ ] set_up_bounds : function to set up some kind of upper and lower bounds on the values? used in the cointainment functions
[X] avoids
[X] avoids_set
[X] involves
[X] involved_in
[ ] involvement_check_final : probably these three are not needed
[ ] involvement_check
[ ] involvement_fits
[X] occurrences
[X] all_intervals : a substition(block/interval) decomposition of the permutation, with all possible blocks(all sizes, also non-maximal), copied as `block_decomposition`
[X] all_monotone_intervals : a substitution(block/interval) decomposition of the permutation where the blocks are monotone increasing or decreasing, copied as `monotone_block_decomposition`
[ ] monotone_quotient : values of the first elements of the blocks in the monotone substitution(block/interval) decomposition
[X] maximal_interval : finds the biggest interval in the permutation
[X] simple_location : finds some interval of length at least 2
[X] is_simple : checks if the permutation is simple
[X] is_strongly_simple : checks if the permutation is strongly? simple
[X] decomposition : another function to do a substitution(block/interval) decomposition, TODO this name is to general
[X] inflate : TODO implement, review permpy implementations
[ ] right_extensions : WTF
[ ] all_right_extensions : WTF
[ ] all_extensions : WTF
[ ] all_extensions_track_index : WTF
[X] plot
[X] _show
[X] to_tikz
[X] shrink_by_one : gives a PermSet of all permutations with one element removed
[X] children : alias for `shrink_by_one`
[X] downset
[X] sum_indecomposable_sequence
[ ] sum_indec_bdd_by : WTF
[X] contains_locations : same as the `occurrences_of` function
[ ] rank_val : inversions containing the location as the bigger element
[ ] rank_encoding : `rank_val` of each position in permutation
[X] num_rtlmax_ltrmin_layers
[X] rtlmax_ltrmin_decomposition
[X] num_inc_bonds : should be copied as `count_inc_bonds`
[X] num_dec_bonds : should be copied as count_dec_bonds
[X] num_bonds : same as `bonds`, should be copied as `count_bonds`
[X] contract_inc_bonds
[X] contract_dec_bonds
[X] contract_bonds
[X] all_syms
[X] is_representative
[ ] greedy_sum : TODO ask J
[ ] chom_sum : TODO ask J
[ ] chom_skew : TODO ask J
