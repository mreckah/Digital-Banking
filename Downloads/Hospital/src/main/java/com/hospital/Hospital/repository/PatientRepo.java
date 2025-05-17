package com.hospital.Hospital.repository;

import com.hospital.Hospital.entities.Patient;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

@Repository
public interface PatientRepo extends JpaRepository<Patient,Integer> {
    Page<Patient>findByName(String keyword, Pageable pageable);
    @Query("select p from Patient p where p.name like :x")
    Page<Patient>check(@Param("x") String keyword, Pageable pageable);

}
