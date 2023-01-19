#Central sweeps get all reps
for swp in sdn ssv
do
    cat header.txt > ${swp}_5.fvec

    for rep in $(seq 0 1000)
    do
        tail -n 1 ../vcfs/${swp}/${rep}/merged.${swp}.win_5.fvec >> ${swp}_5.fvec
    done
done

#Subsampled 10% for the linked sweeps

for win in 0 1 2 3 4 6 7 8 9 10
do
    for swp in sdn ssv
    do
        cat header.txt > ${swp}_${win}.fvec

        for rep in $(seq 0 1000)
        do
            tail -n 1 ../vcfs/${swp}/${rep}/merged.${swp}.win_${win}.fvec >> ${swp}_${win}.fvec
        done
    done


#Condense all neutrals
cat header.txt > neuts.fvec
for rep in $(seq 0 10000)
do
    tail -n 1 ../vcfs/neut/${rep}/merged.neut.win_5.fvec >> neuts.fvec
done